import { providerFixture } from "./providerFixture.tsx";

export const kidneyStudyFixture = {
  id: 1,
  provider_study_name: "Kidney Cancer Detection",
  hospital_id: 1,
  provider_study_id: "236",
  provider_id: 1,
  created_at: "2021-03-01T00:00:00.000Z",
  study_configuration_id: 1,
  study_configuration: {
    id: 1,
    name: "Kidney Cancer Detection",
    tag: "kidney_cancer_detection",
    step_configurations: [],
    version: "1.0.0",
    provider_id: 1
  },
  provider: providerFixture
};
