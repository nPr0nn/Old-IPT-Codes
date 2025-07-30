import matplotlib.pyplot as plt
import Class_CSVReader
import scipy.integrate as it
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
from mpl_toolkits import mplot3d
from scipy.optimize import curve_fit
import numpy as np
import math
import csv
import time

from frisbee_flight_simu.frisbee_disc import Frisbee_Disc
from frisbee_flight_simu.physics_model import Coeff_Model

plt.rcParams["font.family"] = "serif"

# Initial Conditions (Standard)
#--------------------------------------------------------------------------------------
# Positions
x_0      =   0.0;
y_0      =   0.0;
z_0      =   1.26;

# Velocities
vx_0     =    11.36;
vy_0     =    0.0;
vz_0     =   -2.66;

# Euler Angles
phi_0    =  0.0;   # roll
theta_0  =  -0.41
# theta_0  =  -(22.3)*(np.pi/180); # pitch
print(theta_0)
gamma_0  =  0.0;   # yaw

# Angular Velocities
dphi_0   =   0.0;
dtheta_0 =   0.0;
dgamma_0 =   10*np.pi;
print(dgamma_0)

# Angle of Atack
alpha_0  = (7)*(np.pi/180)
print(alpha_0)

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }
#=======================================================================================================================

def save_data(result):
     header = ['x', 'y', 'z', 'phi', 'theta', 'gamma', 'time'];
     with open('simu_data.csv', 'w', encoding='UTF8', newline='') as f:
          writer = csv.writer(f);
          # writer.writerow(header);
          for i in range(len(result.x)):
               row = []
               row.append(result.x[i]);
               row.append(result.y[i]);
               row.append(result.z[i]);
               row.append(result.phi[i]);
               row.append(result.theta[i]);
               row.append(result.gamma[i]);
               row.append(result.times[i]);
               writer.writerow(row);
               print(row);
     return

#=======================================================================================================================

def checkAirbounce_plot_colormap(parameter_to_change, parameter_array):
     n = len(parameter_array);

     unit_dict = {"vx": "m/s", "vz": "m/s", "phi": "rad", "theta": "rad", "dgamma": "rad/s"};
     parameter_label = {"vx": r'$\dot{x}_0$', "vz": r'$\dot{z}_0$', "phi": r'$\phi_0$', "theta": r'$\theta_0$', "dgamma":
                        r'$\dot{\gamma}_0$'};

     parameter_dict = {"vx": 0, "vz": 1, "phi": 2, "theta": 3, "dgamma": 4};
     p = [];
     p.append(vx_0);
     p.append(vz_0);
     p.append(phi_0);
     p.append(theta_0);
     p.append(dgamma_0);

     color_map = []
     label_var_theta = []
     label_var_time  = []

     for i in range(len(parameter_array)):
          lin = []
          p[parameter_dict[parameter_to_change]] = parameter_array[i];
          frisbee = Frisbee_Disc(x=x_0, y=y_0, z=z_0, vx=p[0], vy=vy_0, vz=p[1], phi=p[2], theta=p[3], gamma=gamma_0, dphi=dphi_0, dtheta=dtheta_0, dgamma=p[4]);
          result  = frisbee.compute_trajectory(flight_time = 4, n_times = 1000);

          eps = 0.0001
          for j in range(len(result.times)):
               if(result.z[j] <= 0.01):
                    lin.append(result.z[j] + 0.98*(-result.z[j]) )
               else:
                    lin.append(result.vz[j])
               # elif(result.vz[j] < 0 and result.vz[j] + eps < -0.01):
                    # lin.append(-1)
               # elif(result.vz[j] > 0 and result.vz[j] - eps > 0.01):
                    # lin.append(1)
               # else:
                    # lin.append(0)
               # lin.append(result.z[j]);

          color_map.append(lin);

     color_map = np.array(color_map);
     fig = plt.figure();
     ax = fig.add_subplot(111);

     shw = ax.imshow(color_map, vmin=-6, vmax=6, interpolation='nearest', aspect="auto", cmap='bwr');

     m = 1000

     ax.xaxis.set_ticks(np.arange(0, m, int(m/10)), fontsize=14)
     ax.xaxis.set_ticklabels([ round(i*(4/m),2) for i in np.arange(0, m, int(m/10))])
     ax.yaxis.set_ticks(np.arange(0, n, int(n/10)), fontsize=14)
     ax.yaxis.set_ticklabels([ round(parameter_array[i],2) for i in np.arange(0, n, int(n/10))])

     ax.set_xlabel("Time(s)", fontdict=font);
     ax.set_ylabel(parameter_label[parameter_to_change] + " (" + unit_dict[parameter_to_change] + ") ", fontdict=font);
     # ax.set_title("Color Map of Frisbee Velocity Direction")
     cbar = plt.colorbar(shw)
     cbar.set_label(r'$\dot{z}$' + " (m/s) ", fontdict=font)
     # ax.clim(-6, 6)
     plt.show();
     # plt.imsave(parameter_to_change + '.png');
     # max_z.clear();

def checkAirbounce():
     var_vx     =   np.arange(20, 2, -0.01);
     var_vz     =   np.arange(0,  -20, -0.01);
     var_phi    =   np.arange(np.pi/2, -np.pi/2, -0.01);
     var_theta  =   np.arange(np.pi/2, -1.24, -0.01);
     var_dgamma =   np.arange(20*np.pi, -20*np.pi, -0.01);

     parameter_dict = {"vx": 0, "vz": 1, "phi": 2, "theta": 3, "dgamma": 4};
     d = [];
     d.append(var_vx);
     d.append(var_vz);
     d.append(var_phi);
     d.append(var_theta);
     d.append(var_dgamma);

     parameter_to_change = "dgamma"
     checkAirbounce_plot_colormap(parameter_to_change, d[parameter_dict[parameter_to_change]]);

def plot_frisbee_possible_trajectories():
     var_vz0 = [2, 0, -2, -20]
     var_colors   = ['#cc5900','#6600cc','#cc0000', '#33132e']

     plt.axhline(y = z_0, color = 'k', linestyle = '--')
     for i in range(len(var_vz0)-1):
          frisbee = Frisbee_Disc(x=x_0, y=y_0, z=z_0, vx=vx_0, vy=vy_0, vz=var_vz0[i], phi=phi_0, theta=theta_0, gamma=gamma_0, dphi=dphi_0, dtheta=dtheta_0, dgamma=dgamma_0);
          result = frisbee.compute_trajectory(flight_time = 2, n_times = 1000);
          plt.plot(result.x, result.z, c = var_colors[i])
          plt.xlabel("Time", fontdict=font)
          plt.ylabel("Frisbee position on " + r'$z$', fontdict=font)
          plt.xticks([])
          plt.yticks([])

     # plt.title("Frisbee height x Flight duration")
     # plt.legend()
     plt.show()


def find_index(times, time):
     for i in range(len(times)):
          if times[i] >  time:
               return i

def plot_forces():
     total_time = 1.5
     # Call Simulation
     #--------------------------------------------------------------------------------------
     forces_coeff = [0.92, 1.62, 0.51, 0.48]
     frisbee = Frisbee_Disc(model=Coeff_Model(forces_coeff, alpha_0),x=x_0, y=y_0, z=z_0, vx=vx_0, vy=vy_0, vz=vz_0,phi=phi_0, theta=theta_0, gamma=gamma_0, dphi=dphi_0, dtheta=dtheta_0, dgamma=dgamma_0);
     result = frisbee.compute_trajectory(flight_time = total_time, n_times = 62);

     csv_reader_tracker          = Class_CSVReader.CSVReader("", "force.csv")
     f_drag, f_up, f_lift, f_g  = csv_reader_tracker.read_csv(0, 1, 2, 3)
     times = result.times

     X_Y_Spline_fup   = make_interp_spline(np.array(times), np.array(f_up))
     X_Y_Spline_fdrag = make_interp_spline(np.array(times), np.array(f_drag))

     times_  = np.linspace(times.min(), times.max(), 500)
     f_up_   = X_Y_Spline_fup(times_)

     # times_  = np.linspace(times.min(), times.max(), 500)
     # f_drag_ = X_Y_Spline_fdrag(f_drag)

     plt.plot(times_, f_up_, label = r'$F_{Lift} - F_{G}$', c="#f2571f")

     # plt.plot(times, f_up, label = r'$F_{Lift} - F_{G}$', c="#cc0000")
     plt.plot(times, f_drag, label = r'$F_{Drag}$', c="#8323ba")
     # plt.plot(times, f_g, label = r'$F_{G}$', c="#d37126")

     plt.xlabel("Time(s)", fontdict=font)
     plt.ylabel("Frisbee Forces "+" (N)", fontdict=font)
     plt.yticks(fontsize=13)
     plt.xticks(fontsize=13)

     plt.legend(fontsize=13);
     plt.show();

def plot_trajectory():
     total_time = 1.5
     # Call Simulation
     #--------------------------------------------------------------------------------------
     forces_coeff = [0.92, 1.62, 0.51, 0.48]
     frisbee = Frisbee_Disc(model=Coeff_Model(forces_coeff, alpha_0),x=x_0, y=y_0, z=z_0, vx=vx_0, vy=vy_0, vz=vz_0,phi=phi_0, theta=theta_0, gamma=gamma_0, dphi=dphi_0, dtheta=dtheta_0, dgamma=dgamma_0);
     result = frisbee.compute_trajectory(flight_time = total_time, n_times = 1000);

     # frisbee_2 = Frisbee_Disc(model=Coeff_Model(forces_coeff, alpha_0),x=x_0, y=y_0, z=z_0, vx=vx_0, vy=vy_0, vz=vz_0,phi=phi_0, theta=theta_0, gamma=gamma_0, dphi=dphi_0, dtheta=dtheta_0, dgamma=-dgamma_0);
     # result_2 = frisbee_2.compute_trajectory(flight_time = total_time, n_times = 1000);

     # save_data(result);
     # return

     # Plot
     #--------------------------------------------------------------------------------------
     times = result.times;
     x, y, z = result.x, result.y, result.z;
     vz = result.vz;

     directory = "../Experimental/data/"
     csv_reader_tracker          = Class_CSVReader.CSVReader(directory, "airbounce_f2.csv")
     times_exp_raw, x_exp_raw, z_exp_raw, vz_exp_raw  = csv_reader_tracker.read_csv(0, 1, 2, 3)

     # print(np.array(np.std(times_exp_raw)))
     # print(np.array(np.std(z_exp_raw)))
     # print(np.array(np.std(vz_exp_raw)))

     times_exp = []
     z_exp     = []
     vz_exp     = []
     for i in range(len(times_exp_raw)):
          # print(times_exp_raw[i])
          times_exp.append(times_exp_raw[i])
          z_exp.append(z_exp_raw[i])
          vz_exp.append(vz_exp_raw[i])
          if(times_exp[i] >= total_time):
               break

     plt.axhline(y = 0, color = 'k', linestyle = '--')
     plt.plot(times, result.vz, label = r'$\dot{z}$', c="#0000cc")
     plt.plot(times, result.vx, label = r'$\dot{x}$', c="#007200")
     plt.plot(times, result.vy, label = r'$\dot{y}$', c="#cc0000")

     # plt.plot(result_2.times, result_2.z, label = "Numerical Solution", c="b")

     # plt.errorbar(times_exp, vz_exp, yerr=0.02, xerr=0.001,label = "Experimental", fmt='o', c="#6600cc", ms=2)
     error = 0.01
     # plt.fill_between(times, result.vz-error, result.vz+error, color='red', alpha=0.2)
     # plt.fill_between(times, result_2.z-error, result_2.z+error, color='blue', alpha=0.2)

     plt.xlabel("Time(s)", fontdict=font)
     plt.ylabel("Frisbee velocity "+" (m/s)", fontdict=font)
     plt.yticks(fontsize=13)
     plt.xticks(fontsize=13)

     # plt.plot(result.x, result.y, label = r'$\dot{z}$', c="#cc0000")
     # plt.plot(result_2.x, result_2.y, label = r'$\dot{y}$', c="#0000cc")
     # plt.xlabel("Position of Frisbee on x (m)", fontdict=font)
     # plt.ylabel("Position of Frisbee on y (m)", fontdict=font)


     # ax = plt.axes(projection='3d');
     # ax.plot3D(x, y, z, c="#cc0000");
     # ax.set_xlabel("x (m)");
     # ax.set_ylabel("y (m)");
     # ax.set_zlabel("z (m)");
     plt.legend(fontsize=13);
     plt.show();

if __name__ == "__main__":
     start_time = time.time()
     # plot_frisbee_possible_trajectories()
     # plot_trajectory()
     # checkAirbounce()
     plot_forces()
     print("--- %s seconds ---" % (time.time() - start_time))
