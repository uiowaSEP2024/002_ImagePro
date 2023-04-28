import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";
import {
  Box,
  VStack,
  Button,
  Flex,
  Divider,
  chakra,
  Grid,
  GridItem,
  Container,
  Heading,
  Link,
} from '@chakra-ui/react';
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import { useState, useEffect } from "react";
import { Chakra_Petch } from "@next/font/google";

interface FeatureProps {
  heading: string;
  text: string;
}

const Feature = ({ heading, text }: FeatureProps) => {
  return (
    <GridItem>
      <chakra.h3 fontSize="xl" fontWeight="600">
        {heading}
      </chakra.h3>
      <chakra.p>{text}</chakra.p>
    </GridItem>
  );
};




function Profile() {
  const {currentUser} = useAuthContext()
  const [jobs, setJobs] = useState<Job[]>([]);
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
          base: 'repeat(1, 1fr)',
          sm: 'repeat(2, 1fr)',
          md: 'repeat(2, 1fr)',
        }}
        gap={4}>
        <GridItem colSpan={1}>
          <Box p="50" w="100%" height="100%" borderWidth='1px' borderRadius='lg' overflow='hidden'>
            <VStack alignItems="flex-start" spacing="20px">
              <chakra.h1 fontSize="10xl" fontWeight="700" color="black">
              {currentUser?.first_name} {currentUser?.last_name}
              </chakra.h1>
              <chakra.h2 fontSize="3xl" fontWeight="700" color="blue.400">
              {currentUser?.email}
              </chakra.h2>
              <chakra.h2 data-testid="role" fontSize="3xl" fontWeight="700" color="red.400">
              {currentUser?.role}
              </chakra.h2>
            </VStack>
          </Box>
        </GridItem>
        <GridItem>
          <Flex>
            <Box p="50" alignItems="centered" w="100%" borderWidth='1px' borderRadius='lg' overflow='hidden'>
              <VStack alignItems="center" spacing="10px">
                <chakra.h3 fontSize="1xl">
                  At BotImage, we strive to provide a fully extensible and scaleable solution to even the most complex jobs.
                  As a valued customer, you've used our site to track 
                </chakra.h3>
                <chakra.h1 alignItems="centered" p="10" fontSize="5xl" fontWeight="700" fontStyle="bold" color="purple.500">
                  {jobs.length} jobs
                </chakra.h1>
              </VStack>
            </Box>
          </Flex>
        </GridItem>
      </Grid>
      <Divider mt={12} mb={12} />
      <Heading fontSize={'3xl'} p="5">Recent Jobs</Heading>
      <Grid
        templateColumns={{
          base: 'repeat(1, 1fr)',
          sm: 'repeat(2, 1fr)',
          md: 'repeat(4, 1fr)',
        }}
        gap={{ base: '8', sm: '12', md: '16' }}>
          {jobs.slice(0,4).map(job => (
            <Box key={job.id} p="10" w="100%" height="100%" borderWidth='1px' borderRadius='lg' overflow='hidden'>
            <chakra.h3>{job.provider_job_name}</chakra.h3>
            <chakra.p>See this job <Link href='/jobs' color='blue.500'> here </Link> </chakra.p>
          </Box>
          ))}
      </Grid>
    </Box>
  );
}

export default withAuthenticated(Profile)