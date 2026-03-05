require("dotenv").config();
const express = require("express");
const cors = require("cors");
const connectDB = require("./config/db");
const newsRoutes = require("./routes/newsRoutes");

const app = express();

connectDB();

app.use(cors());
app.use(express.json());

app.use("/api", newsRoutes);

app.listen(process.env.PORT, () =>
  console.log("Server running on port", process.env.PORT)
);