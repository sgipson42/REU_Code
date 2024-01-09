import json
import seaborn as sns
import datetime
import matplotlib.pyplot as plt

def main():
    files = [['no2', 'NO2_2019_forest_5x5_area.json'], ['co', 'CO_2019_forest_5x5_area.json']]
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/pollution/graphs/'
    chems = {'NO2':[], 'CO':[]}

    for filename in files: #no2 file, co file
        poln = filename[0] #no2, co
        with open(filename[1], 'r') as f:
            data = json.load(f)
            for i in data:
                properties = i['properties']
                conc = properties[poln] #no2, co
                if poln == 'no2': #add to no2 if no2
                    chems['NO2'].append(conc)
                else: #add to co if not no2
                    chems['CO'].append(conc)

    #print(chems)
    #fig, ax = plt.subplots()
    #ax.boxplot(chems.values(), widths = (0.5, 0.5))
    #ax.set_xticklabels(chems.keys())
    #ax.set_xlabel('Pollutant')
    #ax.set_ylabel('Concentration (mol/m2)')
    #ax.set_title('2019 Pollutant Concentrations at Ground Truth Area')
    #ax.grid(True)
    #plt.savefig(png_filepath + 'box_plot_5x5_2019.png')
    #sns.set_palette("colorblind")
    colorblind_palette = sns.color_palette("colorblind")
    #c = 'brown'
    c = colorblind_palette[0]
    fig, ax1 = plt.subplots(figsize=(8, 6))
    no2_plot = ax1.boxplot(chems['NO2'], positions=[1], widths=0.6, notch = True, patch_artist = True, boxprops=dict(facecolor=c, color=c), capprops=dict(color=c), whiskerprops=dict(color=c), flierprops=dict(color=c, markeredgecolor=c),medianprops=dict(color=c))
    ax1.set_ylabel('NO2 Concentration (mol/m2)', color=c)
    ax1.tick_params(axis='y', labelcolor=c)
    ax1.set_xticks([])

    # Create a secondary y-axis and plot the second box plot on it
    #c = 'darkgoldenrod'
    c = colorblind_palette[1]
    ax2 = ax1.twinx()
    co_plot = ax2.boxplot(chems['CO'], positions=[2], widths=0.6, notch = True, patch_artist = True, boxprops=dict(facecolor=c, color=c), capprops=dict(color=c), whiskerprops=dict(color=c), flierprops=dict(color=c, markeredgecolor=c),medianprops=dict(color=c))
    ax2.set_ylabel('CO Concentration (mol/m2)', color=c)
    ax2.tick_params(axis='y', labelcolor=c)
    ax2.set_xticks([])

    # Customize the box plots
    #colors = ['tab:blue', 'tab:orange']
    #for plot, color in zip([no2_plot, co_plot], colors):
     #   for box in plot['boxes']:
     #       box.set(facecolor=color, alpha=0.5)
     #   for whisker in plot['whiskers']:
     #       whisker.set(color=color)
     #   for cap in plot['caps']:
     #       cap.set(color=color)
     #   for median in plot['medians']:
     #       median.set(color=color)
     #   for flier in plot['fliers']:
     #       flier.set(markerfacecolor=color)

    # Set x-axis labels
    ax1.set_xticks([1, 2])
    ax1.set_xticklabels(['NO2', 'CO'])
    ax1.set_title('2019 Pollutant Concentrations at Ground Truth Area')
    plt.savefig(png_filepath + 'box_plot_5x5_2019.png')

main()
