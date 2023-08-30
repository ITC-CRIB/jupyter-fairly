import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { 
  createDatasetCommandPlugin,
  cloneDatasetCommandPlugin, 
} from './dataset';
import {editMetadataPlugin} from './metadata'
import { uploadDatasetPlugin} from './upload';
import { FairlyMenuPlugin } from './menu';

/**
 *  Activate jupyter-fairly extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@jupyter-fairly:plugin',
  autoStart: true,
  requires : [],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyter-fairly is activated!');
      
    }
};


export default [
  plugin, 
  createDatasetCommandPlugin, 
  editMetadataPlugin, 
  uploadDatasetPlugin,
  cloneDatasetCommandPlugin,
  FairlyMenuPlugin,
];

