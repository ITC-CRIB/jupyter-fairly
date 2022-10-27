import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { createDatasetCommandPlugin } from './dataset';
import {editMetadataPlugin} from './metadata'
import {archiveDatasetPlugin} from './archive';

/**
 *  Activate jupyterfair extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:plugin',
  autoStart: true,
  requires : [],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, 
    settingRegistry: ISettingRegistry | null) => {
    console.log('jupytefair is activated!!');
  }
};

export default [
  plugin, 
  createDatasetCommandPlugin, 
  editMetadataPlugin, 
  archiveDatasetPlugin];
