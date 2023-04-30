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
  Td
} from "@chakra-ui/react";
import NextLink from "next/link";
import React, { useMemo } from "react";
import { useState, useEffect } from "react";

const columns = [
  { name: "Job No.", uid: "reference_number" },
  { name: "Name", uid: "name" },
  { name: "Provider", uid: "provider_name" },
  { name: "Status", uid: "status" }
];

type JobTableCellProps = {
  job: Job;
  colId: (typeof columns)[number]["uid"];
};

const JobTableCell: React.FC<JobTableCellProps> = ({ job, colId }) => {
  if (!job) return null;

  if (colId === "name") {
    return <Text>{job.provider_job_name} </Text>;
  }

  if (colId === "reference_number") {
    return (
      <Link as={NextLink} href={`/jobs/${job.id}`} passHref>
        <Text>{job.id} ↗</Text>
      </Link>
    );
  }

  if (colId === "provider_name") {
    return <Text>--</Text>;
  }

  if (colId === "status") {
    return <Text>--</Text>;
  }

  return null;
};

function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);

  const [search, setSearch] = React.useState("");

  const handleSearch = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setSearch(event.target.value);
  };

  useEffect(() => {
    async function loadJobs() {
      const data = await fetchJobs();
      if (data) {
        setJobs(data);
      }
    }
    loadJobs();
  }, []);

  const filteredJobs = useMemo(() => {
    return jobs
      .slice()
      .filter(
        (item) =>
          item.provider_job_name.toLowerCase().includes(search.toLowerCase()) ||
          String(item.id).includes(search)
      );
  }, [jobs, search]);

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

export default withAuthenticated(Jobs);
