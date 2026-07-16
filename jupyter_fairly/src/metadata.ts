import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  editIcon,
} from '@jupyterlab/ui-components';

import { PathExt } from '@jupyterlab/coreutils';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { showErrorMessage } from '@jupyterlab/apputils';

export const editMetadataPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-fairly:metadata',
  requires: [IDefaultFileBrowser],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    defaultFileBrowser: IDefaultFileBrowser
  ) => {
    const fileBrowserModel = defaultFileBrowser.model;

    // Open the manifest.yalm file in the file editor
    const openManifestCommand = "openManifestCommand"
    app.commands.addCommand(openManifestCommand, {
      label: 'Edit Dataset Metadata',
      isEnabled: () => true,
      isVisible: () => true, // TODO: set depending if the dataset is initiated or not
      icon: editIcon,
      execute: () => {

        // manager.open() takes a contents API path (forward slashes,
        // relative to the server root, no './' prefix)
        const pathManifest = PathExt.join(fileBrowserModel.path, 'manifest.yaml');
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
      rank: 101
    });
  }
};
