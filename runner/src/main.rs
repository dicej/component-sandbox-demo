use {
    anyhow::{anyhow, Result},
    clap::Parser,
    sha2::{Digest, Sha256},
    std::path::Path,
    tokio::fs,
    wasmtime::{
        component::{Component, Linker},
        Config, Engine, Store,
    },
};

#[derive(Parser)]
pub struct Options {
    component: String,
    statements: Vec<String>,
    expression: String,
}

wasmtime::component::bindgen!({
    path: "../wit/sandbox.wit",
    world: "sandbox",
    async: true
});

#[tokio::main]
async fn main() -> Result<()> {
    let options = Options::parse();

    let mut config = Config::new();
    config.wasm_component_model(true);
    config.async_support(true);

    let engine = Engine::new(&config)?;

    let linker = Linker::new(&engine);
    let mut store = Store::new(&engine, ());

    let cwasm = {
        // Reuse or create cached .cwasm file.

        let wasm_path = Path::new(&options.component);

        let wasm = fs::read(&wasm_path).await?;

        let mut digest = Sha256::new();
        digest.update(&wasm);
        let wasm_hash = digest.finalize();

        let cwasm_path = wasm_path
            .parent()
            .ok_or_else(|| anyhow!("expected component path to have a parent directory"))?
            .join(format!("{}.cwasm", hex::encode(&wasm_hash)));

        if let Ok(cwasm) = fs::read(&cwasm_path).await {
            cwasm
        } else {
            let body = engine.precompile_component(&wasm)?;
            fs::write(&cwasm_path, &body).await?;
            body
        }
    };

    let instance = linker
        .instantiate_async(&mut store, &unsafe {
            Component::deserialize(&engine, &cwasm)
        }?)
        .await?;

    let sandbox = Sandbox::new(&mut store, &instance)?;

    for statement in options.statements {
        sandbox
            .call_exec(&mut store, &statement)
            .await?
            .map_err(|s| anyhow!("exec error: {s}"))?;
    }

    println!(
        "result: {}",
        sandbox
            .call_eval(&mut store, &options.expression)
            .await?
            .map_err(|s| anyhow!("eval error: {s}"))?
    );

    Ok(())
}
