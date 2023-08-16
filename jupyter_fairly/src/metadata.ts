import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  editIcon,
} from '@jupyterlab/ui-components';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { showErrorMessage } from '@jupyterlab/apputils';

export const editMetadataPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-fairly:edit-meta',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("editMetadataPlugin activated!!");
    // const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowser = fileBrowserFactory.tracker.currentWidget;
    const fileBrowserModel = fileBrowser.model;

    // Open the manifest.yalm file in the file editor
    const openManifestCommand = "openManifestCommand"
    app.commands.addCommand(openManifestCommand, {
      label: 'Edit Dataset Metadata',
      isEnabled: () => true,
      isVisible: () => true, // TODO: set depending if the dataset is initiated or not
      icon: editIcon,
      execute: () => {

        
        let currentPath = './'.concat(fileBrowserModel.path);
        const pathManifest = currentPath.concat('/manifest.yaml');
        /* We assume that the current directory contains the
        manifest.yalm, if not we show an error message
         */
        try {
          fileBrowserModel.manager.open(pathManifest)
        } catch (error: any) {
          // TODO: customize error type
          showErrorMessage("Error Opening manifest.yalm", error);
        };
        
      }
    });

    app.contextMenu.addItem({
      command: openManifestCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 105
    });
  }
};
