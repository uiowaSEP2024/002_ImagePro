/**
 * This file contains the Studies component of the application.
 * The Studies component is a React component that displays a list of all studies in the system.
 * It fetches the studies data from the server, filters the studies based on the user's search input, and displays the studies in a table.
 * Each row in the table represents a study and contains the study's name, provider, status, and a link to the study's details page.
 */

// Import necessary libraries, components, hooks, and types.
import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";
import { fetchStudies, fetchProviderById, fetchHospitalById } from "@/data";
import { Study } from "@/data/types";
import {
  Input,
  Container,
  Text,
  Heading,
  Link,
  TableContainer,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  Tag
} from "@chakra-ui/react";
import NextLink from "next/link";
import React, { useMemo, useEffect, useState } from "react";

/**
 * The Studies component is a React component that displays a list of all studies in the system.
 * It fetches the studies data from the server, filters the studies based on the user's search input, and displays the studies in a table.
 * Each row in the table represents a study and contains the study's name, provider, status, and a link to the study's details page.
 */
function Studies() {
  // Initialize state variables for the studies data and the search input.
  const [studies, setStudies] = useState<Study[]>([]);
  const [search, setSearch] = useState("");
  const [providerNames, setProviderNames] = useState<{ [key: string]: string }>({});
  const [hospitalNames, setHospitalNames] = useState<{ [key: string]: string }>({});
  const { currentUser } = useAuthContext();

  // Define the columns for the studies table.
  let columns: { name: string; uid: string }[] = [];

  if (currentUser) {
    if (currentUser.role == "admin") {
      columns = [
        { name: "Study No.", uid: "reference_number" },
        { name: "Name", uid: "name" },
        { name: "Hospital", uid: "hospital_name" },
        { name: "Provider", uid: "provider_name" },
        { name: "Status", uid: "status" }
      ];
    } else if (currentUser.role == "provider") {
      columns = [
        { name: "Study No.", uid: "reference_number" },
        { name: "Name", uid: "name" },
        { name: "Hospital", uid: "hospital_name" },
        { name: "Status", uid: "status" }
      ];
    } else {
      columns = [
        { name: "Study No.", uid: "reference_number" },
        { name: "Name", uid: "name" },
        { name: "Provider", uid: "provider_name" },
        { name: "Status", uid: "status" }
      ];
    }
  }

  /**
   * The StudyTableCell component is a React component that displays a cell in the studies table.
   * It takes a study and a column ID as props, and displays the appropriate data for the cell based on the column ID.
   */
  type StudyTableCellProps = {
    study: Study;
    colId: (typeof columns)[number]["uid"];
  };

  const StudyTableCell: React.FC<StudyTableCellProps> = ({ study, colId }) => {
    useEffect(() => {
      studies.forEach((study) => {
        if (study.provider_id && !providerNames[study.id]) {
          fetchProviderById(study.provider_id).then((data) => {
            if (data) {
              setProviderNames((prev) => ({
                ...prev,
                [study.id]: data.provider_name,
              }));
            }
          });
        }
      });
    }, [studies]);

    const providerName = providerNames[study.id];

    useEffect(() => {
      studies.forEach((study) => {
        if (study.hospital_id && !hospitalNames[study.id]) {
          fetchHospitalById(study.hospital_id).then((data) => {
            if (data) {
              setHospitalNames((prev) => ({
                ...prev,
                [study.id]: data.hospital_name,
              }));
            }
          });
        }
      });
    }, [studies]);

    const hospitalName = hospitalNames[study.id];

    if (!study) return null;

    if (colId === "name") {
      return <Text>{study.study_configuration.name} </Text>;
    }

    if (colId === "reference_number") {
      return (
        <Link as={NextLink} href={`/studies/${study.id}`} passHref>
          <Text>{study.id} ↗</Text>
        </Link>
      );
    }

    if (colId === "hospital_name") {
      return <Text>{hospitalName}</Text>;
    }

    if (colId === "provider_name") {
      return <Text>{providerName}</Text>;
    }

    if (colId === "status") {
      const numCompletedSteps = study.events?.filter(
        (event) => event.kind === "Complete"
      ).length;
      const numSteps = study.study_configuration.step_configurations.length;
      const status = numCompletedSteps === numSteps ? "Done" : "Waiting";
      return (
        <Tag colorScheme={status === "Done" ? "green" : "yellow"}>{status}</Tag>
      );
    }

    return null;
  };

  // Define the function to handle changes to the search input.
  const handleSearch = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setSearch(event.target.value);
  };

  // Fetch the studies data when the component mounts.
  useEffect(() => {
    async function loadStudies() {
      const data = await fetchStudies();
      if (data) {
        setStudies(data);
      }
    }
    loadStudies();
  }, []);

  // Filter the studies based on the user's search input.
  const filteredStudies = useMemo(() => {
    return studies.slice().filter((item) => {
      const studyNameMatches = item.study_configuration.name.toLowerCase().includes(search.toLowerCase());
      const studyIdMatches = String(item.id).includes(search);
      const providerNameMatches = providerNames[item.id] && providerNames[item.id].toLowerCase().includes(search.toLowerCase());
      const hospitalNameMatches = hospitalNames[item.id] && hospitalNames[item.id].toLowerCase().includes(search.toLowerCase());

      // Return true if any of the conditions match
      return studyNameMatches || studyIdMatches || providerNameMatches || hospitalNameMatches;
    });
  }, [studies, search, providerNames, hospitalNames]);

  // Render the Studies component.
  return (
    <Container pt={8} maxW={"container.lg"}>
      <Heading>Studies</Heading>

      <Input
        variant="flushed"
        data-testid="search"
        placeholder="Search studies..."
        width="100%"
        onChange={handleSearch}
      />

      <TableContainer mt={8}>
        <Table role="grid" variant="simple" aria-label="Studies">
          <Thead>
            <Tr>
              {columns.map((column) => (
                <Th fontSize={"sm"} pl={1} key={column.uid}>
                  {column.name}
                </Th>
              ))}
            </Tr>
          </Thead>

          <Tbody>
            {filteredStudies.map((study) => (
              <Tr key={study.id}>
                {columns.map((column) => (
                  <Td pl={1} key={column.uid}>
                    <StudyTableCell study={study} colId={column.uid} />
                  </Td>
                ))}
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
    </Container>
  );
}

/**
 * Export the Studies component wrapped with the withAuthenticated higher-order component.
 */
export default withAuthenticated(Studies);
