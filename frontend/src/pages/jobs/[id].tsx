import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchEvents, fetchJobById } from "@/data";
import { Job, JobEvent } from "@/data/types";
import { useEnsureAuthenticated } from "@/hooks/useAuthContext";
import {
  Container,
  Loading,
  Progress,
  Spacer,
  Table,
  Text,
  Tooltip,
} from "@nextui-org/react";
import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useMemo, useState } from "react";

const columns = [
  { name: "Event No.", uid: "event_number" },
  { name: "Name", uid: "name" },
  { name: "Kind", uid: "kind" },
  { name: "Date", uid: "date" },
  { name: "Time", uid: "time" },
];

type ColumnName = typeof columns[number]["uid"];

type JobEventWithNumber = JobEvent & { event_number: number };

function JobPage({ initialIsPageLoading = true }) {
  useEnsureAuthenticated()
  const router = useRouter();
  const { id: jobId } = router.query;
  const [events, setEvents] = useState<JobEventWithNumber[]>([]);
  const [job, setJob] = useState<Job | null>(null);
  const [isPageLoading, setIsPageLoading] = useState(initialIsPageLoading);

  useEffect(() => {
    async function loadJob() {
      const data = await fetchJobById(jobId as unknown as number);
      if (data) setJob(data);
    }

    if (jobId) {
      loadJob();
    }
  }, [jobId]);

  // Derive the jobStatus based on the last event
  // If the last event is an error, the job is in an error state
  // If the job has num_steps, check if the number of step events matches the number of steps
  // Otherwise, check if the job has a complete event
  const jobStatus = useMemo(() => {
    const lastEvent = events.at(-1);

    if (lastEvent?.kind === "error") {
      return "error";
    }

    if (job?.num_steps) {
      const numStepEvents = events.filter(
        (event) => event.kind === "step"
      ).length;
      return numStepEvents === job.num_steps ? "success" : "pending";
    }

    const hasCompleteEvent = events.some((event) => event.kind === "complete");
    return hasCompleteEvent ? "success" : "pending";
  }, [events, job]);

  useEffect(() => {
    const loadJobEvents = async () => {
      try {
        const data = await fetchEvents(jobId as unknown as number);
        if (!data) {
          return true;
        }

        setEvents(
          data.map((event, index) => ({ ...event, event_number: index + 1 }))
        );
      } catch (e) {
        console.log(e);
      }

      setIsPageLoading(false);
    };

    const interval = setInterval(async () => {
      await loadJobEvents();
      if (jobStatus === "success") {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [job, jobId, jobStatus]);

  const renderCell = (event: JobEventWithNumber, column: ColumnName) => {
    switch (column) {
    case "name":
      return <Text>{event.name}</Text>;
    case "kind":
      return <Text>{event.kind}</Text>;
    case "date":
      return event.created_at ? (
        <Text>{new Date(event.created_at).toISOString().split("T")[0]}</Text>
      ) : null;
    case "time":
      return event.created_at ? (
        <Text>{new Date(event.created_at).toLocaleTimeString()}</Text>
      ) : null;

    case "event_number":
      return <Text>{event.event_number}</Text>;
    default:
      return null;
    }
  };

  // Derive the progress percentage based on either job.num_steps
  // if it is available, or do 0 -> 1 -> 50 -> 100 based on the presence of any events
  const progressAmount = useMemo(() => {
    if (job?.num_steps) {
      const stepEvents = events.filter((event) => event.kind === "step");
      return ((stepEvents.length / job?.num_steps) * 100).toFixed(0);
    }

    if (jobStatus === "success") {
      return 100;
    }

    if (events.length) {
      return 50;
    }

    return 1;
  }, [job, jobStatus, events]);

  // Derive the color of the progress bar based on computed job status
  const progressColor = useMemo(() => {
    if (jobStatus === "error") {
      return "error";
    }
    return "success";
  }, [jobStatus]);

  // Don't show page until we have attempted to load some events
  if (isPageLoading) {
    return (
      <Container
        css={{ height: "100%", width: "100%" }}
        alignItems="center"
        justify="center"
      >
        <Loading />
      </Container>
    );
  }

  return (
    <>
      <Container gap={2} justify="center" css={{ paddingTop: "$4" }}>
        <Link href={"/jobs"}>&lt; Jobs</Link>
        <Text h1 align-items="center">
          Job #{jobId} - {job?.provider_job_name}
        </Text>
        <Text h4>Progress</Text>
        <Tooltip
          style={{ width: "100%" }}
          content={`${progressAmount}% complete`}
        >
          <Progress
            color={progressColor}
            striped
            value={Number(progressAmount)}
          />
        </Tooltip>

        <Spacer />
        <Text h4>Events</Text>
        <Table
          lined
          bordered
          shadow={false}
          color="primary"
          aria-label="Events"
          css={{
            height: "auto",
            minWidth: "100%",
            zIndex: 1,
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

export default withAuthenticated(JobPage);