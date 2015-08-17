# Plotting Results
Once the MapReduce jobs contained in the sentiment_analysis directory are complete, the final step is to visualize the results for easy distribution and summarization. This directory includes both the code required to accomplish this, as well as copies of all the generated visualizations (as .png files).  Plots following the `fc_XXXX.png` naming scheme depict the top fearmongers for a particular topic (where XXXX represents the topic).  Plots following the `fig_ts_XXXX.png` pattern show how relative levels of fear about a topic shift over time.

## Explanation of Contents
### Code Files
- **plot_count.py**: Generates `fc_XXXX.png` files to show top fearmongers by topic using results of MapReduce jobs stored on S3 and matplotlib
- **plot_ts.py**: Uses a similar approach to plot changes in fear content over time and plots results in `fig_ts_XXXX.png` files.
