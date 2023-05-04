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
  Link,
  Text,
  Icon,
  IconButton
} from "@chakra-ui/react";
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import { useState, useEffect, useMemo, useCallback } from "react";

import NextLink from "next/link";
import { FiCopy, FiInfo } from "react-icons/fi";

function Profile() {
  const { currentUser } = useAuthContext();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [copied, setCopied] = useState(false);

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

  const isCustomer = currentUser?.role === "customer";

  const onCopyId = useCallback(() => {
    if (!currentUser) return;
    navigator.clipboard.writeText(currentUser.id.toString());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [currentUser]);

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
            height={"full"}
            p="50"
            w="100%"
            height="100%"
            borderWidth="1px"
            borderRadius="lg"
            overflow="hidden"
          >
            <VStack
              position={"relative"}
              alignItems="flex-start"
              spacing="20px"
            >
              <Heading fontSize="6xl" fontWeight="700" color="black">
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
                {currentUser?.role}{" "}
                {isCustomer ? `(id: #${currentUser.id})` : ""}
              </Heading>

              {isCustomer &&
                (copied ? (
                  <Text fontSize="sm" color="green.500">
                    Copied to clipboard!
                  </Text>
                ) : (
                  <Flex gap={1} color={"gray"} alignItems={"baseline"}>
                    <Text fontSize="sm">
                      Copy and share your unique ID with your provider to use
                      their services.
                    </Text>
                    <IconButton
                      icon={<Icon onClick={onCopyId} as={FiCopy} />}
                      aria-label={"copy-id-button"}
                      variant={"ghost"}
                      m={0}
                      p={0}
                      minH={0}
                      minW={0}
                      h={0}
                    />
                  </Flex>
                ))}
            </VStack>
          </Box>
        </GridItem>
        <GridItem>
          <Flex height={"full"}>
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
      <Heading fontSize={"3xl"} py="5">
        Recent Jobs
      </Heading>
      <Flex
        direction={{ base: "column", md: "row" }}
        gap={{ base: "2", sm: "4", md: "8" }}
      >
        {reversedJobs.length === 0 && (
          <Text fontSize={"1xl"} textAlign={"center"}>
            No jobs found.
          </Text>
        )}
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
            <Heading>{job.job_configuration.name} </Heading>
            <Text>#{job.id}</Text>
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
