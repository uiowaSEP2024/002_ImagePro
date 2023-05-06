module.exports = {
    resolve: {
      extensions: [".tsx", ".ts", ".js"]
    },
    node: {
      fs: "empty",
      child_process: "empty",
      readline: "empty"
    },
    module: {
      rules: [{
          test: /\.spec.ts$/,
          exclude: [/node_modules/],
          use: [{
            loader: "ts-loader"
          }]
        },
        {
          test: /\.feature$/,
          use: [{
            loader: "./node_modules/@badeball/cypress-cucumber-preprocessor/loader"
          }]
        }
      ]
    }
  };