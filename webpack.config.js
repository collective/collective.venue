process.traceDeprecation = true;
const path = require("path");
const package_json = require("./package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const webpack_config =
  require("@patternslib/dev/webpack/webpack.config").config;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");

module.exports = () => {
  let config = {
    entry: {
      "bundle.min": path.resolve(__dirname, "resources/index"),
    },
  };

  config = webpack_config({
    config: config,
    package_json: package_json,
  });
  config.output.path = path.resolve(
    __dirname,
    "src/collective/venue/resources/collective-venue-bundle/",
  );
  config.plugins.push(
    mf_config({
      name: package_json.name,
      filename: "remote.min.js",
      remote_entry: config.entry["bundle.min"],
      dependencies: {
        ...package_json_patternslib.dependencies,
        ...package_json.dependencies,
      },
    }),
  );

  if (process.env.NODE_ENV === "development") {
    config.devServer.port = "8012";
    config.devServer.static.directory = path.resolve(__dirname, "resources/");
  }

  return config;
};
