import React, { useEffect, useMemo } from "react";
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

const COLORS_LIST = [
  "rgb(255, 99, 132)",
  "rgb(75, 192, 192)",
  "rgb(53, 162, 235)",
  "rgb(89, 23, 235)",
  "rgb(125, 69, 200)"
];

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

type JobsChartProps = {
  year?: number;
  jobs?: Job[];
};

const JobsChart: React.FC<JobsChartProps> = ({
  year = new Date().getFullYear(),
  jobs = []
}) => {
  const jobsForYear = useMemo(() => {
    return jobs.filter((job) => {
      return new Date(job.created_at!).getFullYear() === Number(year);
    });
  }, [jobs, year]);

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

  return <Bar data={data} options={options} />;
};

export default JobsChart;
