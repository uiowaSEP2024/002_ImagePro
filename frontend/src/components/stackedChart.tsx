import React, { useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { useState } from "react";
import { fetchJobs } from "@/data";
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

const colorsList = ['rgb(255, 99, 132)', 'rgb(75, 192, 192)', 'rgb(53, 162, 235)', 'rgb(89, 23, 235)', 'rgb(125, 69, 200)'];

const JobsChart = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [counts, setCounts] = useState<Record<string, number[]>>({});

  useEffect(() => {
    const getJobs = async () => {
      const data = await fetchJobs();
      if (data) {
        setJobs(data);
        const _counts: Record<string, number[]> = {};

        data.forEach(({ job_configuration, created_at }) => {
          const name = job_configuration.name || "Other";
          const month = new Date(created_at!).getMonth();

          if (!_counts[name]) {
            _counts[name] = Array(12).fill(0);
          }
          _counts[name][month]++;
        });

        // Set counts to use later
        setCounts(_counts);
      }
    };
    getJobs();
  }, []);

  const labels = [
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
  const options = {
    plugins: {
      title: {
        display: true,
        text: "Stacked Chart: Number of Jobs every month for 2022",
      },
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
        title: {
          display: true,
          text: "Month",
        },
      },
      y: {
        stacked: true,
        title: {
          display: true,
          text: "Number of Jobs",
        },
      },
    },
  };

  const data = {
    labels: labels.slice(0, new Date(Date.now()).getMonth() + 1),
    datasets: Object.entries(counts).map(([key, value], idx) => {
      return {
        label: key,
        data: value,
        backgroundColor: colorsList[idx],
      };
    }),
  };
  return <Bar data={data} options={options} />;
};

export default JobsChart;
