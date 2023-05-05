
import { defineConfig } from 'cypress';
import webpackPreprocessor from '@cypress/webpack-preprocessor';
import { addCucumberPreprocessorPlugin } from '@badeball/cypress-cucumber-preprocessor';


async function setupNodeEvents(on: any, config: any) {
  await addCucumberPreprocessorPlugin(on, config);

  const options = {
    webpackOptions: {
      module: {
        rules: [
          {
            test: /\.feature$/,
            use: [
              {
                loader: '@badeball/cypress-cucumber-preprocessor/webpack',
                options: config,
              },
            ],
          },
        ],
      },
    },

  };

  on('file:preprocessor', webpackPreprocessor(options));

  return config;
}

module.exports = {
  default: defineConfig({
    e2e: {
      baseUrl: 'http://localhost:3000',
      specPattern: '**/features/*.feature',
      supportFile: false,
      setupNodeEvents,
    },
  }),
};