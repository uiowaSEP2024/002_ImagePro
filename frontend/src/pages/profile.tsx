import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";
import {
  Box,
  VStack,
  Flex,
  Divider,
  chakra,
  Grid,
  GridItem,
  Container,
  Heading,
  Link
} from "@chakra-ui/react";
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import { useState, useEffect, useMemo } from "react";

import NextLink from "next/link";

function Profile() {
  const { currentUser } = useAuthContext();
  const [jobs, setJobs] = useState<Job[]>([]);

  const reversedJobs = useMemo(() => jobs.slice().reverse(), [jobs]);

  useEffect(() => {
    async function loadJobs() {
      const data = await fetchJobs();
      if (data) {
        setJobs(data);
      }
    }
    loadJobs();
  }, []);

  return (
    <Box as={Container} maxW="7xl" mt={14} p={4}>
      <Grid
        templateColumns={{
          base: "repeat(1, 1fr)",
          sm: "repeat(2, 1fr)",
          md: "repeat(2, 1fr)"
        }}
        gap={4}
      >
        <GridItem colSpan={1}>
          <Box
            p="50"
            w="100%"
            height="100%"
            borderWidth="1px"
            borderRadius="lg"
            overflow="hidden"
          >
            <VStack alignItems="flex-start" spacing="20px">
              <Heading fontSize="10xl" fontWeight="700" color="black">
                {currentUser?.first_name} {currentUser?.last_name}
              </Heading>
              <Heading fontSize="3xl" fontWeight="700" color="blue.400">
                {currentUser?.email}
              </Heading>
              <Heading
                data-testid="role"
                fontSize="3xl"
                fontWeight="700"
                color="red.400"
              >
                {currentUser?.role}
              </Heading>
            </VStack>
          </Box>
        </GridItem>
        <GridItem>
          <Flex>
            <Box
              p="50"
              alignItems="centered"
              w="100%"
              borderWidth="1px"
              borderRadius="lg"
              overflow="hidden"
            >
              <VStack alignItems="center" spacing="10px">
                <Heading fontSize="xl">
                  At BotImage, we strive to provide a fully extensible and
                  scalable solution to even the most complex jobs. As a valued
                  customer, you have used our site to track
                </Heading>
                <Heading
                  alignItems="centered"
                  p="10"
                  fontSize="5xl"
                  fontWeight="700"
                  fontStyle="bold"
                  color="purple.500"
                >
                  {jobs.length} jobs
                </Heading>
              </VStack>
            </Box>
          </Flex>
        </GridItem>
      </Grid>
      <Divider mt={12} mb={12} />
      <Heading fontSize={"3xl"} p="5">
        Recent Jobs
      </Heading>
      <Flex
        direction={{ base: "column", md: "row" }}
        gap={{ base: "2", sm: "4", md: "8" }}
      >
        {reversedJobs.slice(0, 4).map((job) => (
          <Box
            key={job.id}
            p="10"
            w="100%"
            height="100%"
            borderWidth="1px"
            borderRadius="lg"
            overflow="hidden"
          >
            <Heading>{job.provider_job_name}</Heading>
            <chakra.p>
              See this job{" "}
              <Link as={NextLink} href={`/jobs/${job.id}`} color="blue.500">
                here
              </Link>
            </chakra.p>
          </Box>
        ))}
      </Flex>
    </Box>
  );
}

export default withAuthenticated(Profile);
