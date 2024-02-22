import { Flex, Circle, Heading, Icon, Center } from "@chakra-ui/react";
import { ArrowForwardIcon } from "@chakra-ui/icons";
import { MdPending } from "react-icons/md";
import { FiCheck, FiX } from "react-icons/fi/index.js";
import { Metadata } from "./Metadata";
import { useEffect, useRef, useState } from "react";

/**
 * Define the kinds of events that can be displayed in the timeline.
 */
const KINDS = {
  pending: "Pending",
  complete: "Complete",
  success: "Success",
  in_progress: "In progress",
  error: "Error",
  info: "Info"
} as const;

type Kind = keyof typeof KINDS;

/**
 * Define the background colors for the different kinds of events.
 */
const bgColors: Record<Kind, string> = {
  complete: "whatsapp.500",
  in_progress: "whatsapp.500",
  pending: "gray.500",
  success: "whatsapp.500",
  error: "red.500",
  info: "gray.500"
};

const CIRCLE_SIZE = "10";
const MINI_CIRCLE_SIZE = "2";
const DEFAULT_TIMELINE_HEIGHT_PX = 40;
const ICON_SIZE = "6";

/**
 * Define the icons for the different kinds of events.
 */
const IconComponents: Record<Kind, React.FC> = {
  complete: () => <Icon as={FiCheck} boxSize={ICON_SIZE} />,
  in_progress: () => <Icon as={FiCheck} boxSize={ICON_SIZE} />,
  success: () => <Icon as={FiCheck} boxSize={ICON_SIZE} />,
  error: () => <Icon as={FiX} boxSize={ICON_SIZE} />,
  info: () => <Circle bg={"gray"} size={"2"} />,
  pending: () => <Icon as={FiCheck} boxSize={ICON_SIZE} />
};

type EventTimelineProps = {
  kind: Kind;
  title: string;
  metadata?: Record<string, any>;
  metadataConfigurations?: any[];
  isLast?: boolean;
};

/**
 * EventTimeline is a functional component that renders an event in a timeline.
 * It supports different kinds of events, including steps, completions, successes, errors, and info.
 * Each kind of event is displayed with a different icon and background color.
 * The event can also include metadata, which is displayed in a table below the event title.
 *
 * @param {object} props - The properties passed to the component.
 * @param {Kind} props.kind - The kind of the event.
 * @param {string} props.title - The title of the event.
 * @param {Record<string, any>} props.metadata - The metadata of the event.
 * @param {boolean} props.isStart - Whether the event is the start of the timeline.
 * @param {any[]} props.metadataConfigurations - The configurations for the metadata.
 * @returns {JSX.Element} The EventTimeline component.
 */
export const EventTimeline: React.FC<EventTimelineProps> = ({
  kind: propKind = "info",
  title,
  metadata,
  isLast,
  metadataConfigurations
}) => {
  const kind = KINDS[propKind] || "info";
  const circleBg = bgColors[kind];
  const circleSize = kind === "info" ? MINI_CIRCLE_SIZE : CIRCLE_SIZE;
  const IconComponent = IconComponents[kind] || IconComponents["info"];
  const metadataRef = useRef<HTMLElement>(null);
  const [timelineHeight, setTimelineHeight] = useState(
    DEFAULT_TIMELINE_HEIGHT_PX
  );

  useEffect(() => {
    if (metadataRef.current) {
      if (metadataRef.current.clientHeight > DEFAULT_TIMELINE_HEIGHT_PX) {
        setTimelineHeight(metadataRef.current.clientHeight);
      } else {
        setTimelineHeight(DEFAULT_TIMELINE_HEIGHT_PX);
      }
    }
  }, [metadata]);

  return (
    <Flex width={"100%"} alignItems={"center"} flex={1} gap={3}>
      <Flex  alignItems={"center"} direction={"row"}>
        <Center width={circleSize}>
          <Circle color={"white"} size={circleSize} bg={circleBg}>
            {<IconComponent />}
          </Circle>
        </Center>
      </Flex>

      <Flex direction={"column"} width={"140px"} >
        <Heading m={0} size={"sm"} fontWeight={"medium"}>
          {title}
        </Heading>
        {!!metadata && (
          <Metadata
            configurations={metadataConfigurations}
            fontSize={"sm"}
            ref={metadataRef}
            metadata={metadata}
          />
        )}
      </Flex>
            <Flex alignItems={"center"} direction={"row"}>
                {!isLast && <Icon as={ArrowForwardIcon} color="gray.500" boxSize={6} />}

        </Flex>
    </Flex>
  );
};
