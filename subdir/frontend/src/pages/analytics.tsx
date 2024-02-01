import { Container, Heading, Select, Spacer, VStack } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";
import JobsChart from "@/components/StackedChart";
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import { useState, useEffect, useMemo } from "react";

function Analytics() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    const getJobs = async () => {
      const data = await fetchJobs();
      if (data) {
        setJobs(data);
      }
    };
    getJobs();
  }, []);

  const availableYears = useMemo(() => {
    return Array.from(
      new Set(
        jobs.reduce((acc, curr) => {
          const year = new Date(curr.created_at!).getFullYear();
          if (!acc.includes(year)) {
            acc.push(year);
          }
          return acc;
        }, [] as number[])
      )
    );
  }, [jobs]);

  const defaultYear = useMemo(() => {
    return availableYears[0];
  }, [availableYears]);

  const [year, setYear] = useState<number>();

  const finalYear = year || defaultYear;

  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <Heading lineHeight={1.5} textAlign={"center"}>
        Analytics
      </Heading>
      <Spacer height="20px" />

      <VStack spacing={4} alignItems={"flex-start"}>
        <Heading>
          Jobs for {finalYear} ({jobs.length})
        </Heading>

        <Select
          marginX={8}
          value={finalYear}
          onChange={(e) => setYear(Number(e.target.value))}
          placeholder="Select option"
        >
          {availableYears.map((year) => {
            return (
              <option key={year} value={year}>
                {year}
              </option>
            );
          })}
        </Select>
        <JobsChart year={finalYear} jobs={jobs} />
      </VStack>
    </Container>
  );
}

export default withAuthenticated(Analytics, ["provider"]);
