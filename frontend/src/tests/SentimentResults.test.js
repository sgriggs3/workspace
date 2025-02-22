import { render, screen } from "@testing-library/react";
import SentimentResults from "../components/SentimentResults";

test("displays granularity selector", () => {
  render(<SentimentResults />);
  expect(screen.getByLabelText("Analysis Level")).toBeInTheDocument();
});
