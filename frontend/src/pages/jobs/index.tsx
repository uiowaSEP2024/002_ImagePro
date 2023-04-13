import { fetchJobs, Job } from "@/data";
import { useEnsureAuthenticated } from "@/hooks/useAuthContext";
import { Container, Table, Text } from "@nextui-org/react";
import NextLink from "next/link";
import { useState, useEffect } from "react";

const columns = [
  { name: "Job No.", uid: "reference_number" },
  { name: "Name", uid: "name" },
  { name: "Provider", uid: "provider_name" },
  { name: "Status", uid: "status" },
  { name: "Actions", uid: "actions" },
];

type ColumnName = typeof columns[number]["name"];
export default function Jobs() {
  useEnsureAuthenticated()
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    async function loadJobs() {
      const data = await fetchJobs();
      if (data) setJobs(data);
    }

    loadJobs();
  }, []);

  const renderCell = (job: Job, column: ColumnName) => {
    switch (column) {
    case "name":
      return <Text>{job.provider_job_name} </Text>;
    case "reference_number":
      return (
        <NextLink href={`/jobs/${job.id}`} passHref>
          <Text>{job.id} ↗️</Text>
        </NextLink>
      );
    case "provider_name":
      return "--";
    case "status":
      return "--";
    default:
      return null;
    }
  };

  return (
    <Container>
      <Text h1>Jobs</Text>
      <Table
        lined
        bordered
        shadow={false}
        color="primary"
        aria-label="Jobs"
        css={{
          height: "auto",
          minWidth: "100%",
        }}
        selectionMode="none"
      >
        <Table.Header columns={columns}>
          {(column) => (
            <Table.Column
              key={column.uid}
              hideHeader={column.uid === "actions"}
              align={column.uid === "actions" ? "center" : "start"}
            >
              {column.name}
            </Table.Column>
          )}
        </Table.Header>

        <Table.Body items={jobs}>
          {(item) => (
            <Table.Row key={item.id}>
              {(column) => (
                <Table.Cell key={column}>
                  {renderCell(item, column as ColumnName)}
                </Table.Cell>
              )}
            </Table.Row>
          )}
        </Table.Body>
      </Table>
    </Container>
  );
}
