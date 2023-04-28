import { Metadata } from "@/components/Metadata";
import { EventTimeline } from "@/components/EventTimeline";
import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchEvents, fetchJobById } from "@/data";
import { Job, JobEvent } from "@/data/types";
import { useEnsureAuthenticated } from "@/hooks/useAuthContext";
import { ArrowBackIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  VStack,
  Heading,
  Progress,
  Tooltip,
  Divider,
  Link,
  Box,
  Text,
  Spinner,
  Center,
  ThemingProps
} from "@chakra-ui/react";
//import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useMemo, useState } from "react";

type JobEventWithNumber = JobEvent & { event_number: number };

function JobPage({ initialIsPageLoading = true }) {
  useEnsureAuthenticated();
  const router = useRouter();
  const { id: jobId } = router.query;
  const [events, setEvents] = useState<JobEventWithNumber[]>([]);
  const [job, setJob] = useState<Job | null>(null);
  const [isPageLoading, setIsPageLoading] = useState(initialIsPageLoading);

  const reversedEvents = useMemo(() => {
    return events.slice().reverse();
  }, [events]);

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
  const progressColorScheme = useMemo((): ThemingProps["colorScheme"] => {
    if (jobStatus === "error") {
      return "red";
    }

    return "whatsapp";
  }, [jobStatus]);

  // Don't show page until we have attempted to load some events
  if (isPageLoading) {
    return (
      <Container alignItems={"center"} maxW="container.lg" py={"6"}>
        <Center>
          <Spinner />
        </Center>
      </Container>
    );
  }

  const jobDetails = {
    "Job Name": job?.provider_job_name,
    "Requested At": new Date().toLocaleTimeString(),
    "Customer ID": job?.customer_id,
    Provider: "-"
  };

  return (
    <>
      <Container maxW="container.lg" py={"6"}>
        <VStack gap={"4"} w={"full"} align="left">
          <Link href={"/jobs"}>
            <Button
              size={"md"}
              fontWeight={"semibold"}
              variant={"link"}
              _hover={{}}
              leftIcon={<ArrowBackIcon />}
            >
            Back to Jobs
            </Button>
          </Link>

          <Tooltip label={`${progressAmount}% complete`}>
            <Progress
              borderRadius={"xl"}
              isAnimated={Number(progressAmount) < 100}
              size="md"
              hasStripe={Number(progressAmount) < 100}
              colorScheme={progressColorScheme}
              value={Number(progressAmount)}
            />
          </Tooltip>

          <Box>
            <Heading fontWeight={"semibold"} size={"lg"} alignItems="center">
            Job #{jobId}
            </Heading>
            <Metadata metadata={jobDetails} />
          </Box>
          <Divider />

          <Center
            alignSelf={"center"}
            data-testid={"events-timeline"}
            flexDirection="column"
            gap={2}
          >
            {reversedEvents.map((event, idx) => {
              return (
                <EventTimeline
                  isStart={idx === events.length - 1}
                  key={event.id}
                  title={event.name}
                  kind={event.kind as any}
                  metadata={event.event_metadata}
                />
              );
            })}
          </Center>
        </VStack>

      </Container>

      <Box align-self={"center"} m={10} >
        <Text align={"center"} >
        Issue with this job? Contact system administrator at <Link href={"https://www.gmail.com"} color={"#0072f5"}>admin@botimage.com</Link>
        </Text>
      </Box>
    </>

  );
}

export default withAuthenticated(JobPage);
