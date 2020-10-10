module.exports = {
    parserPreset: {
        parserOpts: {
            headerPattern: /^(\[\w*\]){1}\s(.+)/,
            headerCorrespondence: ["type", "subject"],
        }
    },
    rules: {
        "header-max-length": [2, "always", 80],
        "type-enum": [2, "always", [
            "[FEATURE]", "[BUGFIX]", "[DOCS]", "[TASK]", "[SECURITY]",
        ]],
        "type-case": [2, "always", "upper-case"],
        "type-empty": [2, "never"],
        "subject-case": [2, "always", "sentence-case"],
        "subject-empty": [2, "never"]
    }
};
