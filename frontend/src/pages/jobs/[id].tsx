import { fetchEvents, fetchJobById, Job, JobEvent } from "@/data";
import {
  Container,
  Progress,
  Spacer,
  Table,
  Text,
  Tooltip,
} from "@nextui-org/react";
import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";

const columns = [
  { name: "Event No.", uid: "event_number" },
  { name: "Name", uid: "name" },
  { name: "Date", uid: "date" },
  { name: "Time", uid: "time" },
];

type ColumnName = typeof columns[number]["uid"];

type JobEventWithNumber = JobEvent & { event_number: number };

export default function JobPage() {
  const router = useRouter();
  const { id: jobId } = router.query;

  const [events, setEvents] = useState<JobEventWithNumber[]>([]);
  const [job, setJob] = useState<Job | null>(null);

  useEffect(() => {
    async function loadJobEvents() {
      const data = await fetchEvents(jobId as string);
      setEvents(
        data.map((event, index) => ({ ...event, event_number: index + 1 }))
      );
    }

    async function loadJob() {
      const data = await fetchJobById(jobId as string);
      setJob(data);
    }

    loadJob();
    loadJobEvents();
  }, [jobId]);

  const renderCell = (event: JobEventWithNumber, column: ColumnName) => {
    switch (column) {
    case "name":
      return <Text>{event.name}</Text>;
    case "date":
      return (
        <Text>{new Date(event.created_at).toISOString().split("T")[0]}</Text>
      );
    case "time":
      return <Text>{new Date(event.created_at).toLocaleTimeString()}</Text>;

    case "event_number":
      return <Text>{event.event_number}</Text>;
    default:
      return null;
    }
  };

  const progress = (0.29 * 100).toFixed(0);

  return (
    <>
      <Container gap={2} justify="center" css={{ paddingTop: "$4" }}>
        <Link href={"/jobs"}>&lt; Jobs</Link>
        <Text h1 align-items="center">
          Job #{jobId} - {job?.provider_job_name}
        </Text>
        <Text h4>Progress</Text>
        <Tooltip style={{ width: "100%" }} content={`${progress}% complete`}>
          <Progress color="success" striped value={Number(progress)} />
        </Tooltip>

        <Spacer />
        <Text h4>Events</Text>
        <Table
          bordered
          shadow={false}
          color="primary"
          aria-label="Events"
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

          <Table.Body items={events}>
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
    </>
  );
}
