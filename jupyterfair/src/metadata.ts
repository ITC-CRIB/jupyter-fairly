import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  editIcon,
} from '@jupyterlab/ui-components';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

export const editMetadataPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:edit-meta',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("editMetadataPlugin activated!!");
    const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowserModel = fileBrowser.model;

    // Open the manifest.yalm file in the file editor
    const openManifestCommand = "openManifestCommand"
    app.commands.addCommand(openManifestCommand, {
      label: 'Edit Dataset Metadata',
      isEnabled: () => true,
      isVisible: () => true, // TODO: set depending if the dataset is initiated or not
      icon: editIcon,
      execute: () => {

        // return relative path w.r.t. jupyter root path.
        // root-path = empty string.
        console.log( `the path is: ${fileBrowserModel.path}`);
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
