import logging

logging.basicConfig(filename='Running_log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [line:%(lineno)d] ')
logger = logging.getLogger('test')
logger.error('test')
logger.info('test')
logger.warning('test')
logger.debug('test')
print('日志记录完毕')
with open('./test.txt','w') as f:
  f.write('hello world')
