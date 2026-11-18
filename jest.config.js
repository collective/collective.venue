const config = require("@patternslib/dev/jest.config.js");

config.roots = ["./resources"];

// Like in Mockup: With pnpm, packages live in node_modules/.pnpm/. Allow
// Patternslib to be transformed there too.
config.transformIgnorePatterns = [
    "/node_modules/(?!.pnpm/)(?!@patternslib/).+\\.[t|j]sx?$",
    "/node_modules/.pnpm/(?!@patternslib)",
];

module.exports = config;
