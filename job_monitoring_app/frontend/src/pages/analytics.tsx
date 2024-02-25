import { Container, Heading, Select, Spacer, VStack } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";
import JobsChart from "@/components/StackedChart";
import { fetchJobs } from "@/data";
import { Job } from "@/data/types";
import { useState, useEffect, useMemo } from "react";
/**
 * The Analytics component is a React component that displays job analytics for a selected year.
 * It fetches job data, calculates the available years from the job data, and allows the user to select a year to view the job analytics for that year.
 * It also wraps the component with the withAuthenticated higher-order component to ensure that only authenticated users can access this component.
 *
 * @returns {JSX.Element} The rendered Analytics component.
 */
function Analytics() {
  /**
   * State variable for the jobs data.
   * @type {Job[]}
   */
  const [jobs, setJobs] = useState<Job[]>([]);

  /**
   * Effect hook for fetching the jobs data when the component mounts.
   */
  useEffect(() => {
    const getJobs = async () => {
      const data = await fetchJobs();
      if (data) {
        setJobs(data);
      }
    };
    getJobs();
  }, []);

  /**
   * Memoized array of available years derived from the jobs data.
   * @type {number[]}
   */
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

  /**
   * Memoized default year derived from the available years.
   * @type {number}
   */
  const defaultYear = useMemo(() => {
    return availableYears[0];
  }, [availableYears]);

  /**
   * State variable for the selected year.
   * @type {number}
   */
  const [year, setYear] = useState<number>();

  /**
   * Final year value, either the selected year or the default year.
   * @type {number}
   */
  const finalYear = year || defaultYear;

  /**
   * Render the Analytics component.
   */
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

/**
 * Export the Analytics component wrapped with the withAuthenticated higher-order component.
 */
export default withAuthenticated(Analytics, ["provider"]);
