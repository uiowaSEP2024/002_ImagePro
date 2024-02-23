import React, { useMemo } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from "chart.js";

import { Job } from "@/data/types";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// Define the colors to be used for the different datasets in the chart.
const COLORS_LIST = [
  "rgb(255, 99, 132)",
  "rgb(75, 192, 192)",
  "rgb(53, 162, 235)",
  "rgb(89, 23, 235)",
  "rgb(125, 69, 200)"
];

// Define the months of the year.
const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

/**
 * JobsChartProps is a type that represents the properties of the JobsChart component.
 * It includes the year and the jobs to be displayed in the chart.
 */
type JobsChartProps = {
  year?: number;
  jobs?: Job[];
};

/**
 * JobsChart is a functional component that renders a bar chart of jobs.
 * The chart displays the number of jobs for each month of a specified year.
 * Each job is represented by a bar in the chart, and the height of the bar corresponds to the number of jobs.
 * The jobs are grouped by their configuration name, and each group is displayed with a different color.
 *
 * @param {object} props - The properties passed to the component.
 * @param {number} props.year - The year to be displayed in the chart.
 * @param {Job[]} props.jobs - The jobs to be displayed in the chart.
 * @returns {JSX.Element} The JobsChart component.
 */
const JobsChart: React.FC<JobsChartProps> = ({
  year = new Date().getFullYear(),
  jobs = []
}) => {
  // Filter the jobs to include only those for the specified year.
  const jobsForYear = useMemo(() => {
    return jobs.filter((job) => {
      return new Date(job.created_at!).getFullYear() === Number(year);
    });
  }, [jobs, year]);

  // Count the number of jobs for each month and configuration name.
  const counts = useMemo(() => {
    return jobsForYear.reduce((acc, curr) => {
      const { job_configuration, created_at } = curr;
      const name = job_configuration.name || "Other";
      const month = new Date(created_at!).getMonth();

      if (!acc[name]) {
        acc[name] = Array(12).fill(0);
      }

      acc[name][month]++;

      return acc;
    }, {} as Record<string, number[]>);
  }, [jobsForYear]);

  // Find the latest month for which there are jobs.
  const latestMonth = useMemo(() => {
    return jobsForYear.reduce((acc, curr) => {
      const { created_at } = curr;
      const month = new Date(created_at!).getMonth();

      if (month > acc) {
        acc = month;
      }

      return acc;
    }, 0);
  }, [jobsForYear]);

  // Define the options for the chart.
  const options: ChartOptions<"bar"> = {
    plugins: {
      title: {
        display: true,
        text: `Number of Jobs every month for ${year}`
      }
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
        title: {
          display: true,
          text: "Months"
        }
      },
      y: {
        stacked: true,
        title: {
          display: true,
          text: "Number of Jobs"
        }
      }
    }
  };

  // Define the data for the chart.
  const data = useMemo(() => {
    return {
      labels: MONTHS.slice(0, latestMonth + 1),
      datasets: Object.entries(counts).map(([key, value], idx) => {
        return {
          label: key,
          data: value,
          backgroundColor: COLORS_LIST[idx]
        };
      })
    };
  }, [counts, latestMonth]);

  // Render the JobsChart component.
  return <Bar data={data} options={options} />;
};

export default JobsChart;
