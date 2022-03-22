# User Stories

As a user:

- I want to archive a dataset directly from my working environment so that I can perform the task without using a web-based GUI provided by the data repository.

  > I have all required information available on the working environment, I don't want to manually enter it again using a GUI.

  > I have to learn how to use the web interface of the repository, which is different almost for each repository.

  > I find using a command line interface (CLI) to create dataset record and upload data more convenient that using a web-based GUI.

    + *What if datasets could be archived by using a CLI tool which is data-repository agnostic?*


- I want to archive a dataset directly from my JupyterLab GUI so that I can perform the task without leaving my working environment.

  > Using the JupyterLab GUI will facilitate how I archive my data, because I will be able to do it directly from my active workspace.

  > I prefer to use JupyterLab GUI instead of a command line interface (CLI).

    + *What if datasets could be archived directly from the JupyterLab GUI in a data-repository agnostic way?*


- I want to store metadata locally so that I can create and update it easily.

  > I want to have the metadata as an integral part of the dataset, so that it is accessible whenever necessary not only through the data repository.

  > I don't want to wait until the end (i.e. archiving to a repository) to start writing metadata.

    + *What if metadata could be created locally and be stored together with data?*


- I want to edit metadata with my favorite text editor/IDE so that I can create and update it easily.

  > I use an IDE to develop my research code, it is much faster for me to use it also to create or update metadata.

  > I don't want to use UI-based forms to enter metadata, I can do it much faster with my text editor.

    + *What if metadata could be stored in a human-readable format that can be edited with a plain text editor?*


- I want to define common information to different datasets only once so that I don't need to type it for each dataset separately.

  > I regularly upload research data and the repository asks me each time information like categories, license, etc., for which I need to enter the same information manually each time.

    + *What if common information could be indicated for multiple datasets only once and used whenever it is required?*


- I want to import metadata available in the documentation (e.g. README file) so that I don't need to manually enter the same information.

  > A README file describing the meaning of data columns, how data must be interpreted, measurement methods, and data quality already exists. I don't want to type or copy/paste this information to create a separate metadata record.

  > I keep the README file up to date. Manually keeping metadata up to date duplicates my work.

    + *What if metadata could be extracted from the documentation and can be kept in sync?*


- I want to import metadata available in the data files so that I don't need to enter the information manually.

  > I don't want to enter "again" information such as data column names and types, geographical extent, etc. which are already available in the files.

  > My dataset grid has the bounding box coordinates of my study area, but the repository only accepts a single coordinate pair. I have to manually calculate the center location coordinates, which is annoying.

  > The data files always include the latest information. Manually keeping metadata up-to-date duplicates the work, it is also challenging because I have many files.

    + *What if metadata could be extracted from the data files and can be kept in sync?*


- I want to identify my dataset collaborators by using their researcher IDs so that I don't need to type their name, surname, institution, email address, etc.

  > My collaborators all have ORCID IDs and their researcher information is publicly available. Why I need to enter all that information again?

    + *What if researcher information could be imported from online resources by using unique researcher identifiers, e.g. ORCID?*


- I want to update the local metadata record with the remote version available on the data repository so that they are synchronized.

  > Metadata available on the repository includes additional information, such as DOI, citation, etc., which I need to manually add to my local metadata.

  > The data steward updated some metadata information, so that they are inline with the standards. I need to update my metadata record to reflect the changes.

    + *What if local metadata record can be updated easily according to the metadata record available on the repository?*


- I want to specify which data files and folders are included in the dataset so that I can manage the dataset easily.

  > Besides dataset related files and folders, I have many others in my active working environment. I need to prepare a 'clean' version of my dataset whenever I need to publish my data, which results in multiple copies of the files and folders.

  > Because the data repository doesn't allow me to replicate the folder structure I have, I have to create an archive file containing all files, which I manually need to indicate.

    + *What if data to be published could be 'selected' quickly so that I don't spend time preparing clean versions for archiving?*


- I want to archive different datasets from the same project environment so that I can publish data from different parts of the study.

  > We generated different open datasets during our project, which we store under our project workspace in a structured manner. For each dataset we need to prepare different dataset 'packages' manually.

    + *What if different datasets can be easily published from the same workspace each having their own metadata records?*


- I want to archive large datasets without upload or connectivity issues so that I can publish my research outputs completely.

  > Uploading large datasets is time-consuming because uploading sometimes fails. I need to monitor the process manually and restart failed uploads.

  > I cannot pause and restart uploading at different sessions, I have to upload everything at once.

    + *What if the uploading of a dataset to the data repository could be paused to be continued another time, and the overall status could be monitored?*


- I want to archive my dataset from my remote working environment so that I don't need to download a local copy and then upload to the repository from my local workstation.

  > I work on a cloud computing platform, I don't want to download everything to upload it again with my not-so-fast Internet connection.

  > I have to keep my web browser open while uploading my dataset, which includes thousands of data files. Remote research environment is online all the time, upload can be done in the background without my involvement.

    + *What if the uploading of a dataset could continue after closing the browser and the overall status could be monitored in the next session, or notification could be received once upload is completed?*


- I want to archive a new version of the dataset with minimum effort so that I can archive not only the final version, but also important intermediate ones.

  > When I have a new version of my dataset, I need to upload all files manually which takes a lot of time.

  > I need to keep track of different versions of my dataset manually, usually creating various backup copies which pile up in time.

    + *What if dataset versioning could be handled locally and new versions could be uploaded to the repository directly?*


- I want to archive my dataset in different repositories so that I fulfill all administrative obligations and have a better visibility.

  > The funding agency and my institution require me to deposit data to different repositories. I have to create dataset records in each repository separately and also upload data, this is duplicate work.

  > Our scientific domain has a specific repository, but I find archiving dataset also to a generalist repository useful as it provides more visibility.

  > Whenever I need to upload my dataset to different repositories, I need to enter different metadata fields as they have different metadata standards.

    + *What if a dataset can be archived to multiple repositories in accordance with their metadata standards only by changing the repository information?*


- I want to clone a dataset from a repository to my working environment easily so that I can explore it quickly.

  > Manually downloading datasets with many or large files requires a lot of effort.

  > The repository allows me to download all files as a single archive file (e.g. ZIP), but it takes a lot of time for the repository to create the archive on demand.

  > If a dataset includes archive files I need to extract them one by one to access archived files and folders. Sometimes there are many such archive files (e.g. for each month of a 40-years dataset).

  > Metadata is usually not included in the files I can download, so I need to record it separately or visit the repository whenever necessary.

  > I can clone a research code repository with a single command line (`git clone <repository_name>`), why I cannot do the same with a research data repository?

    + *What if a dataset can be cloned to the working environment by using a CLI tool which is data-repository agnostic?*


- I want to clone a dataset from a repository directly to my JupyterLab workspace so that I can explore it quickly.

  > Using the JupyterLab GUI will facilitate how I access the data, because I will be able to do it directly from my active workspace.

  > I prefer to use JupyterLab GUI instead of a command line interface (CLI).

    + *What if a dataset can be cloned to the JupyterLab workspace in a data-repository agnostic way?*
