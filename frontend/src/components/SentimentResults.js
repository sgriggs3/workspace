// frontend/src/components/SentimentResults.js
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";

const SentimentResults = () => {
  const [granularity, setGranularity] = useState("comment");
  const { data } = useSelector((state) => state.sentiment);

  useEffect(() => {
    // Fetch data based on selected granularity
  }, [granularity]);

  return (
    <div>
      <select
        value={granularity}
        onChange={(e) => setGranularity(e.target.value)}
        className="p-2 border rounded-lg"
      >
        <option value="comment">Comment Level</option>
        <option value="video">Video Level</option>
        <option value="channel">Channel Level</option>
      </select>
      {/* Render visualization based on granularity */}
    </div>
  );
};

export default SentimentResults;
