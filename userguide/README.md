### City of Austin Innovation Office

# Data Preparation Tool Guide🏷️

---

### Opening a file

First step is to open a file. Data Preparation accepts both **CSV** and **Excel** files. When opening a CSV file or an Excel document with a single page, the results will be loaded into the main table.

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

The Custom option allows for any value to be in place of null values.

<img title="" src="img\replacenull.jpg" alt="IMAGE" width="435">

### Describe

ToDo

### Rename selected column

Renames the currently selected column. The active column can be selected by either clicking the header or clicking any row under that column. A popup will show allowing entry for a new column name.

### Delete selected column

Deletes the currently selected column. The active column can be selected by either clicking the header or clicking any row under that column. A popup will show allowing entry for a new column name.