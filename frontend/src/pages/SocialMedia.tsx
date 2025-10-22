import { useState, useEffect } from 'react';
import axios from 'axios';
import { Facebook, Send, CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface FacebookStatus {
  connected: boolean;
  page_name: string | null;
  page_id: string | null;
  access_token_valid: boolean;
}

interface ContentPost {
  id: number;
  caption: string;
  image_path: string | null;
  status: string;
  scheduled_time: string | null;
  posted_time: string | null;
  fb_post_id: string | null;
}

export default function SocialMedia() {
  const [fbStatus, setFbStatus] = useState<FacebookStatus | null>(null);
  const [scheduledPosts, setScheduledPosts] = useState<ContentPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [posting, setPosting] = useState(false);
  const [selectedPost, setSelectedPost] = useState<ContentPost | null>(null);

  useEffect(() => {
    fetchFacebookStatus();
    fetchScheduledPosts();
  }, []);

  const fetchFacebookStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/social/facebook/status`);
      setFbStatus(response.data);
    } catch (error) {
      console.error('Error fetching Facebook status:', error);
      setFbStatus({
        connected: false,
        page_name: null,
        page_id: null,
        access_token_valid: false
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchScheduledPosts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/content/scheduled`);
      setScheduledPosts(response.data.filter((p: ContentPost) => p.status === 'scheduled'));
    } catch (error) {
      console.error('Error fetching scheduled posts:', error);
    }
  };

  const handleManualPost = async (postId: number) => {
    if (!confirm('Bạn có chắc muốn đăng bài này lên Facebook ngay?')) return;

    try {
      setPosting(true);
      const response = await axios.post(`${API_URL}/api/social/facebook/post/${postId}`);

      if (response.data.success) {
        alert('Đã đăng bài thành công lên Facebook!');
        await fetchScheduledPosts();
      }
    } catch (error: any) {
      console.error('Error posting to Facebook:', error);
      alert(error.response?.data?.detail || 'Lỗi khi đăng bài lên Facebook');
    } finally {
      setPosting(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'posted': return 'text-green-600 bg-green-50 border-green-200';
      case 'failed': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'scheduled': return 'Đã lên lịch';
      case 'posted': return 'Đã đăng';
      case 'failed': return 'Thất bại';
      default: return status;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Đang tải...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
          <Facebook className="w-8 h-8 text-blue-600" />
          Quản Lý Facebook
        </h1>
        <p className="text-gray-600 mt-2">Kết nối và đăng bài lên fanpage Facebook</p>
      </div>

      {/* Facebook Connection Status */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4">Trạng Thái Kết Nối</h2>

        {fbStatus?.connected ? (
          <div className="flex items-start gap-4">
            <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <div className="text-lg font-medium text-gray-900">Đã kết nối với Facebook</div>
              <div className="text-sm text-gray-600 mt-1">
                Fanpage: <span className="font-semibold">{fbStatus.page_name}</span>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Page ID: {fbStatus.page_id}
              </div>
              <div className="mt-3">
                {fbStatus.access_token_valid ? (
                  <span className="inline-flex items-center gap-1 px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm">
                    <CheckCircle className="w-4 h-4" />
                    Access Token hợp lệ
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm">
                    <XCircle className="w-4 h-4" />
                    Access Token hết hạn
                  </span>
                )}
              </div>
            </div>
            <button
              onClick={fetchFacebookStatus}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Kiểm tra lại
            </button>
          </div>
        ) : (
          <div className="flex items-start gap-4">
            <XCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-1" />
            <div className="flex-1">
              <div className="text-lg font-medium text-gray-900">Chưa kết nối Facebook</div>
              <div className="text-sm text-gray-600 mt-1">
                Cần cấu hình Facebook API để đăng bài tự động
              </div>
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="text-sm text-yellow-800">
                  <strong>Hướng dẫn:</strong>
                  <ol className="list-decimal list-inside mt-2 space-y-1">
                    <li>Tạo Facebook App tại developers.facebook.com</li>
                    <li>Lấy Access Token cho fanpage</li>
                    <li>Cập nhật .env với FACEBOOK_PAGE_ACCESS_TOKEN</li>
                    <li>Khởi động lại backend</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Manual Mode Notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-blue-800">
            <strong>Chế độ đăng thủ công (Manual Mode):</strong> Ứng dụng đang ở chế độ đăng bài thủ công.
            Bạn cần nhấn nút "Đăng ngay" để đăng bài lên Facebook. Tự động đăng theo lịch hiện đang tắt.
          </div>
        </div>
      </div>

      {/* Scheduled Posts */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Bài Đã Lên Lịch</h2>
          <button
            onClick={fetchScheduledPosts}
            className="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Làm mới
          </button>
        </div>

        {scheduledPosts.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Chưa có bài nào được lên lịch</p>
        ) : (
          <div className="space-y-4">
            {scheduledPosts.map(post => (
              <div
                key={post.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-4">
                  {post.image_path && (
                    <img
                      src={post.image_path}
                      alt="Post preview"
                      className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
                    />
                  )}

                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4 mb-2">
                      <p className="text-sm text-gray-700 line-clamp-3">{post.caption}</p>
                      <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(post.status)} whitespace-nowrap`}>
                        {getStatusLabel(post.status)}
                      </span>
                    </div>

                    {post.scheduled_time && (
                      <div className="text-sm text-gray-600 mb-3">
                        Lên lịch: {new Date(post.scheduled_time).toLocaleString('vi-VN')}
                      </div>
                    )}

                    {post.fb_post_id && (
                      <div className="text-xs text-green-600 mb-3 flex items-center gap-1">
                        <CheckCircle className="w-3 h-3" />
                        Đã đăng lên Facebook (ID: {post.fb_post_id})
                      </div>
                    )}

                    <div className="flex gap-2">
                      {post.status === 'scheduled' && !post.fb_post_id && (
                        <button
                          onClick={() => handleManualPost(post.id)}
                          disabled={posting || !fbStatus?.connected}
                          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2 text-sm"
                        >
                          <Send className="w-4 h-4" />
                          {posting ? 'Đang đăng...' : 'Đăng ngay'}
                        </button>
                      )}

                      {post.fb_post_id && (
                        <a
                          href={`https://facebook.com/${post.fb_post_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-4 py-2 bg-blue-50 text-blue-600 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors flex items-center gap-2 text-sm"
                        >
                          <Facebook className="w-4 h-4" />
                          Xem trên Facebook
                        </a>
                      )}

                      <button
                        onClick={() => setSelectedPost(post)}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                      >
                        Chi tiết
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Post Detail Modal */}
      {selectedPost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">Chi Tiết Bài Đăng</h3>
              <button
                onClick={() => setSelectedPost(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              {selectedPost.image_path && (
                <div>
                  <img
                    src={selectedPost.image_path}
                    alt="Post content"
                    className="w-full rounded-lg border border-gray-200"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Caption:</label>
                <p className="bg-gray-50 p-4 rounded-lg border border-gray-200 whitespace-pre-wrap">
                  {selectedPost.caption}
                </p>
              </div>

              {selectedPost.scheduled_time && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Thời gian lên lịch:</label>
                  <p className="text-gray-900">
                    {new Date(selectedPost.scheduled_time).toLocaleString('vi-VN')}
                  </p>
                </div>
              )}

              {selectedPost.posted_time && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Đã đăng lúc:</label>
                  <p className="text-gray-900">
                    {new Date(selectedPost.posted_time).toLocaleString('vi-VN')}
                  </p>
                </div>
              )}

              {selectedPost.fb_post_id && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Facebook Post ID:</label>
                  <p className="text-gray-900 font-mono text-sm bg-gray-50 p-2 rounded">
                    {selectedPost.fb_post_id}
                  </p>
                </div>
              )}

              <div className="flex gap-3 pt-4 border-t">
                {selectedPost.status === 'scheduled' && !selectedPost.fb_post_id && fbStatus?.connected && (
                  <button
                    onClick={() => {
                      handleManualPost(selectedPost.id);
                      setSelectedPost(null);
                    }}
                    disabled={posting}
                    className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 flex items-center justify-center gap-2"
                  >
                    <Send className="w-4 h-4" />
                    Đăng lên Facebook
                  </button>
                )}

                {selectedPost.fb_post_id && (
                  <a
                    href={`https://facebook.com/${selectedPost.fb_post_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center gap-2"
                  >
                    <Facebook className="w-4 h-4" />
                    Xem trên Facebook
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
