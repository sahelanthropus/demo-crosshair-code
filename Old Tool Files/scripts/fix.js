import fs from "fs";
import path from "path";

const root = "./submodules/demoparser2/src/wasm/www/pkg";
let script = fs.readFileSync(path.join(root, "demoparser2.js"), "utf8");
if (!script.includes("export { wasm_bindgen };")) {
	script += "\nexport { wasm_bindgen };";
	fs.writeFileSync(path.join(root, "demoparser2.js"), script);
}
