
import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import { Container, Table, Text } from "@nextui-org/react";
import NextLink from "next/link";
import React from "react";
import { useState, useEffect } from "react";

const columns = [
  { name: "Job No.", uid: "reference_number" },
  { name: "Name", uid: "name" },
  { name: "Provider", uid: "provider_name" },
  { name: "Status", uid: "status" },
  { name: "Actions", uid: "actions" },
];

type ColumnName = typeof columns[number]["name"];
function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);

  const [search, setSearch] = React.useState('');

  const handleSearch = (event: { target: { value: React.SetStateAction<string>; }; }) => {
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

  function filterJobs(jobs: Job[]) {
    return jobs.filter((item) => 
      (item.provider_job_name.toLowerCase().includes(search.toLowerCase()) || String(item.id).includes(search)))
  }

  return (

    <Container>

      <Text h1>Jobs</Text>

        <label htmlFor="search" style={{display: "block", padding: "10px"}} >  
          <input id="search" data-testid="search" type="text" placeholder="Search jobs..." onChange={handleSearch} />
          <br/>
        </label>

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
        id="myTable"
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

        <Table.Body items={filterJobs(jobs)}>
          {(item) => (
            <Table.Row key={item.id}>
              {(column) => (
                <Table.Cell data-testid="job1" key={column}>
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


export default withAuthenticated(Jobs);
