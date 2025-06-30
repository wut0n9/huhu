import React, { useState, useCallback } from 'react';
import { Upload, Button, message, Modal, List, Progress } from 'antd';
import { UploadOutlined, FileTextOutlined, DeleteOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/lib/upload';
import { formatFileSize, isValidFileType, isValidFileSize } from '@/utils/helpers';
import { MAX_FILE_SIZE, SUPPORTED_FILE_TYPES } from '@/utils/constants';
import { UploadedFile } from '@/types/chat';

const { Dragger } = Upload;

interface FileUploadProps {
  onFileUpload: (file: File) => Promise<void>;
  uploadedFiles: UploadedFile[];
  onFileRemove: (fileId: string) => void;
}

interface UploadingFile {
  file: File;
  progress: number;
  status: 'uploading' | 'success' | 'error';
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileUpload,
  uploadedFiles,
  onFileRemove,
}) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [uploadingFiles, setUploadingFiles] = useState<UploadingFile[]>([]);

  const beforeUpload = useCallback((file: RcFile) => {
    if (!isValidFileType(file)) {
      message.error('不支持的文件类型！');
      return false;
    }

    if (!isValidFileSize(file, MAX_FILE_SIZE)) {
      message.error(`文件大小不能超过 ${formatFileSize(MAX_FILE_SIZE)}！`);
      return false;
    }

    return false; // 阻止自动上传
  }, []);

  const handleFileSelect = useCallback(async (file: RcFile) => {
    const uploadingFile: UploadingFile = {
      file,
      progress: 0,
      status: 'uploading',
    };

    setUploadingFiles(prev => [...prev, uploadingFile]);

    try {
      // 模拟上传进度
      const progressInterval = setInterval(() => {
        setUploadingFiles(prev => 
          prev.map(f => 
            f.file === file 
              ? { ...f, progress: Math.min(f.progress + 10, 90) }
              : f
          )
        );
      }, 200);

      await onFileUpload(file);

      clearInterval(progressInterval);
      setUploadingFiles(prev => 
        prev.map(f => 
          f.file === file 
            ? { ...f, progress: 100, status: 'success' }
            : f
        )
      );

      message.success(`${file.name} 上传成功！`);
    } catch (error) {
      setUploadingFiles(prev => 
        prev.map(f => 
          f.file === file 
            ? { ...f, status: 'error' }
            : f
        )
      );
      message.error(`${file.name} 上传失败！`);
    }
  }, [onFileUpload]);

  const handleRemoveFile = useCallback((fileId: string) => {
    onFileRemove(fileId);
    // uploadingFiles 只影响上传中，不影响已上传
    setUploadingFiles(prev => prev.filter(f => f.file.name !== fileId));
  }, [onFileRemove]);

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return <FileTextOutlined style={{ color: '#ff4d4f' }} />;
      case 'doc':
      case 'docx':
        return <FileTextOutlined style={{ color: '#1890ff' }} />;
      case 'txt':
        return <FileTextOutlined style={{ color: '#52c41a' }} />;
      case 'md':
        return <FileTextOutlined style={{ color: '#722ed1' }} />;
      default:
        return <FileTextOutlined />;
    }
  };

  return (
    <>
      <Button
        icon={<UploadOutlined />}
        size="small"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
        onClick={() => setIsModalVisible(true)}
        title="上传文件"
      >
      </Button>

      <Modal
        title="文件上传"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        width={600}
      >
        <div style={{ marginBottom: 16 }}>
          <Dragger
            beforeUpload={beforeUpload}
            onChange={(info) => {
              if (info.file.status === 'removed') {
                return;
              }
              if (info.file.originFileObj) {
                handleFileSelect(info.file.originFileObj);
              }
            }}
            accept={SUPPORTED_FILE_TYPES.join(',')}
            multiple
            showUploadList={false}
          >
            <p className="ant-upload-drag-icon">
              <UploadOutlined />
            </p>
            <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
            <p className="ant-upload-hint">
              支持 PDF、Word、TXT、Markdown 等格式，单个文件不超过 10MB
            </p>
          </Dragger>
        </div>

        {/* 上传中的文件 */}
        {uploadingFiles.length > 0 && (
          <div style={{ marginBottom: 16 }}>
            <h4>上传中...</h4>
            {uploadingFiles.map((uploadingFile) => (
              <div key={uploadingFile.file.name} style={{ marginBottom: 8 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  {getFileIcon(uploadingFile.file.name)}
                  <span style={{ flex: 1 }}>{uploadingFile.file.name}</span>
                  <Button
                    size="small"
                    icon={<DeleteOutlined />}
                    onClick={() => handleRemoveFile(uploadingFile.file.name)}
                  />
                </div>
                <Progress
                  percent={uploadingFile.progress}
                  status={uploadingFile.status === 'error' ? 'exception' : undefined}
                  size="small"
                />
              </div>
            ))}
          </div>
        )}

        {/* 已上传的文件 */}
        {uploadedFiles.length > 0 && (
          <div>
            <h4>已上传文件</h4>
            <List
              size="small"
              dataSource={uploadedFiles}
              renderItem={(file) => (
                <List.Item
                  actions={[
                    <Button
                      key="remove"
                      size="small"
                      icon={<DeleteOutlined />}
                      onClick={() => handleRemoveFile(file.file_id)}
                    >
                      删除
                    </Button>
                  ]}
                >
                  <List.Item.Meta
                    avatar={getFileIcon(file.filename)}
                    title={file.filename}
                    description={formatFileSize(file.size)}
                  />
                </List.Item>
              )}
            />
          </div>
        )}
      </Modal>
    </>
  );
};

export default FileUpload; 