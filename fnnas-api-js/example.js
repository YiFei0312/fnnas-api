// 启动示例 
// node example.js 1 基本信息
// node example.js 2 获取存储信息
// node example.js 3 列出文件
// node example.js 4 上传文件 …… 请将文件的硬编码路径替换为你的 包括FnOsClient.js文件中的硬编码
const { MainClient, FnOsClient } = require('./index.js');

async function example1_basic_usage() {
  const client = new MainClient();
  console.log('=== 示例1: 基本信息 ===');
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    console.log('连接成功');
    
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    console.log('登录成功');
    
    const userInfo = await client.user_info();
    console.log('用户信息:', userInfo);
    
    await client.close();
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function example2_get_storage() {
  console.log('=== 示例2: 获取存储信息 ===');
  const client = new MainClient();
  
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    
    const storageInfo = await client.get_user_storage();
    console.log('存储信息:', JSON.stringify(storageInfo, null, 2));
    
    await client.close();
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function example3_list_files() {
  console.log('=== 示例3: 列出文件 ===');
  const client = new FnOsClient();
  
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    
    const fileList = await client.fileList('vol1');
    console.log('文件列表:', JSON.stringify(fileList, null, 2));
    
    await client.close();
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function example4_upload_file() {
  console.log('=== 示例4: 上传文件 ===');
  const client = new FnOsClient();
  
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    
    const result = await client.upload(
      './test.txt',
      '/vol1/1000/sample/test.txt',
      1
    );
    console.log('上传结果:', result);
    
    await client.close();
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function example5_search_files() {
  console.log('=== 示例5: 搜索文件 ===');
  const client = new FnOsClient();
  
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    
    const searchResult = await client.file_search('test', ['/vol1/1000/sample']);
    console.log('搜索结果:', JSON.stringify(searchResult, null, 2));
    
    await client.close();
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function example6_change_port_settings() {
  console.log('=== 示例6: 修改端口设置 ===');
  const client = new MainClient();
  
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    
    const result = await client.setting_port({
      force_https: false,
      redirect: true,
      http_port: 5666,
      https_port: 5667
    });
    console.log('端口设置结果:', result);
    
    await client.close();
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function example7_file_observer() {
  console.log('=== 示例7: 文件监听同步 ===');
  const client = new FnOsClient();
  
  try {
    await client.connect(process.env.FN_WS_URL || 'ws://127.0.0.1:5666/websocket');
    await client.login(process.env.fn_username || '', process.env.fn_password || '');
    
    await client.start_observer({
      nas_path: '/home/sync',
      local_path: './local_sync',
      recursive: true,
      interval: 10
    });
  } catch (error) {
    console.error('错误:', error.message);
  }
}

async function run_all_examples() {
  console.log('请选择要运行的示例:');
  console.log('1. 基本使用（连接、登录、获取用户信息）');
  console.log('2. 获取存储信息');
  console.log('3. 列出文件');
  console.log('4. 上传文件');
  console.log('5. 搜索文件');
  console.log('6. 修改端口设置');
  console.log('7. 文件监听同步');
  console.log('0. 运行所有示例');
  
  const choice = process.argv[2] || '1';
  
  switch (choice) {
    case '1':
      await example1_basic_usage();
      break;
    case '2':
      await example2_get_storage();
      break;
    case '3':
      await example3_list_files();
      break;
    case '4':
      await example4_upload_file();
      break;
    case '5':
      await example5_search_files();
      break;
    case '6':
      await example6_change_port_settings();
      break;
    case '7':
      await example7_file_observer();
      break;
    case '0':
      await example1_basic_usage();
      await example2_get_storage();
      await example3_list_files();
      break;
    default:
      console.log('无效的选择');
  }
}

run_all_examples();
