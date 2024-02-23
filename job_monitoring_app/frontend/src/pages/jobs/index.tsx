/**
 * This file contains the Jobs component of the application.
 * The Jobs component is a React component that displays a list of all jobs in the system.
 * It fetches the jobs data from the server, filters the jobs based on the user's search input, and displays the jobs in a table.
 * Each row in the table represents a job and contains the job's name, provider, status, and a link to the job's details page.
 */

// Import necessary libraries, components, hooks, and types.
import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import {
  Input,
  Container,
  Text,
  Heading,
  Link,
  TableContainer,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  Tag
} from "@chakra-ui/react";
import NextLink from "next/link";
import React, { useMemo } from "react";
import { useState, useEffect } from "react";

// Define the columns for the jobs table.
const columns = [
  { name: "Job No.", uid: "reference_number" },
  { name: "Name", uid: "name" },
  { name: "Provider", uid: "provider_name" },
  { name: "Status", uid: "status" }
];

/**
 * The JobTableCell component is a React component that displays a cell in the jobs table.
 * It takes a job and a column ID as props, and displays the appropriate data for the cell based on the column ID.
 */
type JobTableCellProps = {
  job: Job;
  colId: (typeof columns)[number]["uid"];
};

const JobTableCell: React.FC<JobTableCellProps> = ({ job, colId }) => {
  if (!job) return null;

  if (colId === "name") {
    return <Text>{job.job_configuration.name} </Text>;
  }

  if (colId === "reference_number") {
    return (
      <Link as={NextLink} href={`/jobs/${job.id}`} passHref>
        <Text>{job.id} ↗</Text>
      </Link>
    );
  }

  if (colId === "provider_name") {
    return <Text>{job.provider.first_name}</Text>;
  }

  if (colId === "status") {
    const numCompletedSteps = job.events?.filter(
      (event) => event.kind === "Complete"
    ).length;
    const numSteps = job.job_configuration.step_configurations.length;
    const status = numCompletedSteps === numSteps ? "Done" : "Waiting";
    return (
      <Tag colorScheme={status === "Done" ? "green" : "yellow"}>{status}</Tag>
    );
  }

  return null;
};

/**
 * The Jobs component is a React component that displays a list of all jobs in the system.
 * It fetches the jobs data from the server, filters the jobs based on the user's search input, and displays the jobs in a table.
 * Each row in the table represents a job and contains the job's name, provider, status, and a link to the job's details page.
 */
function Jobs() {
  // Initialize state variables for the jobs data and the search input.
  const [jobs, setJobs] = useState<Job[]>([]);
  const [search, setSearch] = React.useState("");

  // Define the function to handle changes to the search input.
  const handleSearch = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setSearch(event.target.value);
  };

  // Fetch the jobs data when the component mounts.
  useEffect(() => {
    async function loadJobs() {
      const data = await fetchJobs();
      if (data) {
        setJobs(data);
      }
    }
    loadJobs();
  }, []);

  // Filter the jobs based on the user's search input.
  const filteredJobs = useMemo(() => {
    return jobs
      .slice()
      .filter(
        (item) =>
          item.job_configuration.name
            .toLowerCase()
            .includes(search.toLowerCase()) || String(item.id).includes(search)
      );
  }, [jobs, search]);

  // Render the Jobs component.
  return (
    <Container pt={8} maxW={"container.lg"}>
      <Heading>Jobs</Heading>

      <Input
        variant="flushed"
        data-testid="search"
        placeholder="Search jobs..."
        width="100%"
        onChange={handleSearch}
      />

      <TableContainer mt={8}>
        <Table role="grid" variant="simple" aria-label="Jobs">
          <Thead>
            <Tr>
              {columns.map((column) => (
                <Th fontSize={"sm"} pl={1} key={column.uid}>
                  {column.name}
                </Th>
              ))}
            </Tr>
          </Thead>

          <Tbody>
            {filteredJobs.map((job) => (
              <Tr key={job.id}>
                {columns.map((column) => (
                  <Td pl={1} key={column.uid}>
                    <JobTableCell job={job} colId={column.uid} />
                  </Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
    </Container>
  );
}

/**
 * Export the Jobs component wrapped with the withAuthenticated higher-order component.
 */
export default withAuthenticated(Jobs);
