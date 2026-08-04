import { createBrowserRouter } from "react-router-dom";
import Landing from "../pages/Landing";
import Login from "../pages/Login";
import Register from "../pages/Register";
import AppLayout from "../layouts/AppLayout";
import Organizations from "../pages/Organizations";
import OrganizationDetails from "../pages/OrganizationDetails";
import ProjectsList from "../pages/ProjectsList";
import CreateProject from "../pages/CreateProject";
import ProjectDetails from "../pages/ProjectDetails";
import EnvironmentsList from "../pages/EnvironmentsList";
import CreateEnvironment from "../pages/CreateEnvironment";
import EditEnvironment from "../pages/EditEnvironment";
import EnvironmentDetails from "../pages/EnvironmentDetails";
import DatabaseConnectionsList from "../pages/DatabaseConnectionsList";
import CreateDatabaseConnection from "../pages/CreateDatabaseConnection";
import EditDatabaseConnection from "../pages/EditDatabaseConnection";
import DatabaseConnectionDetails from "../pages/DatabaseConnectionDetails";
import ApisList from "../pages/ApisList";
import ProtectedRoute from "./ProtectedRoute";
import GuestRoute from "./GuestRoute";

export const router = createBrowserRouter([
  { path: "/", element: <Landing /> },
  {
    element: <GuestRoute />,
    children: [
      { path: "/login", element: <Login /> },
      { path: "/register", element: <Register /> },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { path: "/organizations", element: <Organizations /> },
          {
            path: "/organizations/:organizationId",
            element: <OrganizationDetails />,
          },
          {
            path: "/organizations/:organizationId/projects",
            element: <ProjectsList />,
          },
          {
            path: "/organizations/:organizationId/projects/new",
            element: <CreateProject />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId",
            element: <ProjectDetails />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments",
            element: <EnvironmentsList />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/new",
            element: <CreateEnvironment />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId",
            element: <EnvironmentDetails />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId/edit",
            element: <EditEnvironment />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId/database-connections",
            element: <DatabaseConnectionsList />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId/database-connections/new",
            element: <CreateDatabaseConnection />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId/database-connections/:connectionId",
            element: <DatabaseConnectionDetails />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId/database-connections/:connectionId/edit",
            element: <EditDatabaseConnection />,
          },
          {
            path: "/organizations/:organizationId/projects/:projectId/environments/:environmentId/apis",
            element: <ApisList />,
          },
        ],
      },
    ],
  },
]);