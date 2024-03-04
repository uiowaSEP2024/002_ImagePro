import { Container, Heading, Select, Spacer, VStack } from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";
import StudiesChart from "@/components/StackedChart";
import { fetchStudies } from "@/data";
import { Study } from "@/data/types";
import { useState, useEffect, useMemo } from "react";
/**
 * The Analytics component is a React component that displays study analytics for a selected year.
 * It fetches study data, calculates the available years from the study data, and allows the user to select a year to view the study analytics for that year.
 * It also wraps the component with the withAuthenticated higher-order component to ensure that only authenticated users can access this component.
 *
 * @returns {JSX.Element} The rendered Analytics component.
 */
function Analytics() {
  /**
   * State variable for the studies data.
   * @type {Study[]}
   */
  const [studies, setStudies] = useState<Study[]>([]);

  /**
   * Effect hook for fetching the studies data when the component mounts.
   */
  useEffect(() => {
    const getStudies = async () => {
      const data = await fetch();
      if (data) {
        setStudies(data);
      }
    };
    getStudies();
  }, []);

  /**
   * Memoized array of available years derived from the studies data.
   * @type {number[]}
   */
  const availableYears = useMemo(() => {
    return Array.from(
      new Set(
        studies.reduce((acc, curr) => {
          const year = new Date(curr.created_at!).getFullYear();
          if (!acc.includes(year)) {
            acc.push(year);
          }
          return acc;
        }, [] as number[])
      )
    );
  }, [studies]);

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
          Studies for {finalYear} ({studies.length})
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
        <StudiesChart year={finalYear} studies={studies} />
      </VStack>
    </Container>
  );
}

/**
 * Export the Analytics component wrapped with the withAuthenticated higher-order component.
 */
export default withAuthenticated(Analytics, ["provider"]);
