import { components } from "@/data/schema";
import {
  Table,
  Tbody,
  Tr,
  Td,
  TableProps,
  Text,
  HStack,
  Link
} from "@chakra-ui/react";
import React from "react";

import NextLink from "next/link";
import { ExternalLinkIcon } from "@chakra-ui/icons";

type MetadataConfiguration = components["schemas"]["MetadataConfiguration"];

/**
 * MetadataProps is a type that represents the properties of the Metadata component.
 * It includes the metadata, configurations, and other properties of the Table component.
 */
type MetadataProps = {
  metadata: Record<string, any>;
  configurations?: MetadataConfiguration[];
} & TableProps;

/**
 * MetadataValue is a functional component that renders a metadata value.
 * It supports different types of values, including units and links.
 *
 * @param {object} props - The properties passed to the component.
 * @param {any} props.value - The value to be rendered.
 * @returns {JSX.Element} The MetadataValue component.
 */
const MetadataValue = (
  props: Partial<MetadataConfiguration> & { value: any }
): JSX.Element => {
  if (props.units) {
    return (
      <HStack spacing={1}>
        <Text>{props.value}</Text>
        <Text fontWeight={"medium"}>{props.units}</Text>
      </HStack>
    );
  }

  if (props.kind == "link") {
    return (
      <Link href={props.value} passHref as={NextLink}>
        <HStack spacing={1}>
          <Text>{props.value}</Text>
          <ExternalLinkIcon mx="2px" mb="2px" />
        </HStack>
      </Link>
    );
  }

  return <Text>{props.value}</Text>;
};

/**
 * Metadata is a functional component that renders a table of metadata.
 * It supports different types of metadata values, including units and links.
 *
 * @param {object} props - The properties passed to the component.
 * @param {Record<string, any>} props.metadata - The metadata to be rendered.
 * @param {MetadataConfiguration[]} props.configurations - The configurations for the metadata.
 * @returns {JSX.Element} The Metadata component.
 */
export const Metadata = React.forwardRef<HTMLElement, MetadataProps>(
  function MetadataRef({ metadata, configurations, ...rest }, ref) {
    const configurationMap = configurations?.reduce((acc, curr) => {
      acc[curr.name] = curr;
      return acc;
    }, {} as Record<string, MetadataConfiguration>);

    return (
      <Table ref={ref} width={"fit-content"} variant={"unstyled"} {...rest}>
        <Tbody>
          {Object.entries(metadata).map(([key, value]) => {
            const configuration = configurationMap?.[key];
            return (
              <Tr key={key}>
                <Td mr={6} pl={0} py={1}>
                  <Text fontSize={"inherit"}>{key}</Text>
                </Td>
                <Td py={1} px={0}>
                  <MetadataValue {...configuration} value={value} />
                </Td>
              </Tr>
            );
          })}
        </Tbody>
      </Table>
    );
  }
);
