import {requestAPI} from './handler';

export function initDataset(rootPath:string, template?: any) {

  let templateMeta = 'default';
  if(template === '4TU.Research' || template === 'Figshare') {
    templateMeta = 'figshare';
  }
  else if (template === 'Zenodo'){
    templateMeta = 'zenodo'
  }

  requestAPI<any>('newdataset', {
    method: 'POST', 
    body: JSON.stringify({
      path: rootPath, 
      template: templateMeta
    })
  }) 
  .then(data => {
    console.log(data);
  })
  .catch(reason => {
    console.error(
      `${reason}`
    );
  });
}


