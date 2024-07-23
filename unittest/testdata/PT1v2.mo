model PT1
  parameter Real T11;
  parameter Real K11;
  parameter Real u0_11;
  Real x11(start=0);
  Modelica.Blocks.Interfaces.RealInput u1;
  Modelica.Blocks.Interfaces.RealOutput y1;
equation
    der(x11) = -1.0 / T11 * x11 + K11 / T11 * (u1 + u0_11);
    y1 = x11;
annotation(
    experiment(StartTime = 0, StopTime = 3600, Tolerance = 1e-06, Interval = 1));
end system;
