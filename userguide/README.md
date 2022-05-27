### City of Austin Innovation Office

# Data Preparation Tool Guide
**Quick links**  
[Opening a file](#opening-a-file) | [Trim Column](#trim-column) | [Set Null Values](#set-null-values) | [Describe](#describe) | [Info](#info) | [Sort](#sort)  
[Change Data Type](#change-data-type)  | [Rename selected column](#rename-selected-column) | [Delete selected column](#delete-selected-column) | [Help button](#help-button) | [Updates](#updates)

### Opening a file

First step is to open a file. Data Preparation Tool accepts both **CSV** and **Excel** files. When opening a CSV file or an Excel document with a single page, the results will be loaded into the main table.

If the Excel file has multiple pages, you will be presented with the **Select Page window**. This will preview the pages in the document. You can go forward and back until you get to the page you'd like to work with, and click on **Open Page**.

<img title="" src="img\selectpage.jpg" alt="IMAGE" width="435">

### Trim Column

The **Trim Column** button will bring up the trim popup window. Here, you can select which values to trim off from the beginning or end of the values in the table. This is useful for data where you need to remove the same information for all values in a column. For example, if the column is full of internet addresses and you wanted to remove the **http://** portion from all of the values, you can drag the trim bar until those letters are red and then hit trim. All values in that column will be updated. 

<img title="" src="img\trim.jpg" alt="IMAGE" width="435">
The first four characters will be trimmed from all values in this column.

### Set Null Values

The **Set Null Values** button will replace all empty values (**nil** by default) with a different value. The popup gives the option to select the following

* Empty
* 0 (Zero)
* Null
* Custom

The Custom option allows for any value to be in place of null values. There are seperate groups for numerical data and text based data. This way numbers and strings can be set to different values.

<img title="" src="img\replacenull.jpg" alt="IMAGE" width="435">

### Describe

The **Describe** button will open up a small window with information describing the current dataset. It is the equivalent of [running .describe in Pandas](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html). There is also a button to export the describe to a CSV file if needed.

<img title="" src="img\Describe.jpg" alt="IMAGE" width="435">

### Info

The **Info** button will open up a small window with information on the dataset such as what data types the columns are and how many non null items are in each column.

<img title="" src="img\info.jpg" alt="IMAGE" width="435">

### Sort

*Sort is currently disabled in this version. In future versions, sort will allow you to sort a column from ascending or descending.*

### Change Data Type

The **Change Data Type** button will attempt to change the data type of the currently selected column. For instance, it'll try to convert a float to int. It cannot change from a text type to a numerical type unless all of the text data is written as numbers (if you have a string column that just has decimals, it should convert these to a float or int). If converting a float to int, it'll attempt to round to the nearest whole number.

### Rename selected column

Renames the currently selected column. The active column can be selected by either clicking the header or clicking any row under that column. A popup will show allowing entry for a new column name.

### Delete selected column

Deletes the currently selected column. The active column can be selected by either clicking the header or clicking any row under that column. A popup will show allowing entry for a new column name.

## Help Button

The help button will open this user guide through the default web browser.

## Updates

The tool will check for new versions on Github when opening. If there is a newer version, a link will appear at the bottom of the window indicating that a new version is available for download.

<img title="" src="img\updates.jpg" alt="IMAGE" width="435">
