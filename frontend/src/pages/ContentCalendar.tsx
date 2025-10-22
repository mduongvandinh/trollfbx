import { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, Clock, Edit, Trash2, Eye, Send, ChevronLeft, ChevronRight } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface ContentPost {
  id: number;
  title: string;
  caption: string;
  content_type: string;
  image_path: string | null;
  status: string;
  scheduled_time: string | null;
  posted_time: string | null;
  created_at: string;
}

type ViewMode = 'month' | 'week';

export default function ContentCalendar() {
  const [posts, setPosts] = useState<ContentPost[]>([]);
  const [drafts, setDrafts] = useState<ContentPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [viewMode, setViewMode] = useState<ViewMode>('month');
  const [selectedPost, setSelectedPost] = useState<ContentPost | null>(null);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [scheduleDateTime, setScheduleDateTime] = useState('');
  const [showEditModal, setShowEditModal] = useState(false);
  const [editCaption, setEditCaption] = useState('');

  useEffect(() => {
    fetchPosts();
    fetchDrafts();
  }, [currentDate]);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/content/scheduled`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching scheduled posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDrafts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/content/drafts`);
      setDrafts(response.data);
    } catch (error) {
      console.error('Error fetching drafts:', error);
    }
  };

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days: (Date | null)[] = [];

    // Add empty cells for days before month starts
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }

    // Add days of month
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(new Date(year, month, i));
    }

    return days;
  };

  const getPostsForDate = (date: Date | null) => {
    if (!date) return [];

    return posts.filter(post => {
      if (!post.scheduled_time) return false;
      const postDate = new Date(post.scheduled_time);
      return postDate.toDateString() === date.toDateString();
    });
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
  };

  const handleSchedulePost = async (postId: number, scheduledTime: string) => {
    try {
      await axios.put(`${API_URL}/api/content/${postId}/schedule`, {
        scheduled_time: scheduledTime
      });
      await fetchPosts();
      await fetchDrafts();
      setShowScheduleModal(false);
      setSelectedPost(null);
      setScheduleDateTime('');
    } catch (error) {
      console.error('Error scheduling post:', error);
      alert('Lỗi khi lên lịch bài đăng');
    }
  };

  const handleUnschedule = async (postId: number) => {
    try {
      await axios.put(`${API_URL}/api/content/${postId}/unschedule`);
      await fetchPosts();
      await fetchDrafts();
    } catch (error) {
      console.error('Error unscheduling post:', error);
      alert('Lỗi khi hủy lịch');
    }
  };

  const handleDeletePost = async (postId: number) => {
    if (!confirm('Bạn có chắc muốn xóa bài đăng này?')) return;

    try {
      await axios.delete(`${API_URL}/api/content/${postId}`);
      await fetchPosts();
      await fetchDrafts();
      setSelectedPost(null);
    } catch (error) {
      console.error('Error deleting post:', error);
      alert('Lỗi khi xóa bài đăng');
    }
  };

  const handleEditPost = async () => {
    if (!selectedPost) return;

    try {
      await axios.put(`${API_URL}/api/content/${selectedPost.id}`, {
        news_id: selectedPost.id,
        caption: editCaption,
        status: selectedPost.status
      });
      await fetchPosts();
      await fetchDrafts();
      setShowEditModal(false);
      setSelectedPost(null);
      setEditCaption('');
    } catch (error) {
      console.error('Error updating post:', error);
      alert('Lỗi khi cập nhật bài đăng');
    }
  };

  const previousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'bg-gray-100 text-gray-700 border-gray-300';
      case 'scheduled': return 'bg-blue-100 text-blue-700 border-blue-300';
      case 'posted': return 'bg-green-100 text-green-700 border-green-300';
      case 'failed': return 'bg-red-100 text-red-700 border-red-300';
      default: return 'bg-gray-100 text-gray-700 border-gray-300';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'draft': return 'Nháp';
      case 'scheduled': return 'Đã lên lịch';
      case 'posted': return 'Đã đăng';
      case 'failed': return 'Thất bại';
      default: return status;
    }
  };

  const days = getDaysInMonth(currentDate);
  const monthName = currentDate.toLocaleDateString('vi-VN', { month: 'long', year: 'numeric' });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Lịch Đăng Bài</h1>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white rounded-lg border border-gray-200 p-1">
            <button
              onClick={() => setViewMode('month')}
              className={`px-4 py-2 rounded ${viewMode === 'month' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
            >
              Tháng
            </button>
            <button
              onClick={() => setViewMode('week')}
              className={`px-4 py-2 rounded ${viewMode === 'week' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
            >
              Tuần
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Navigation */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={previousMonth}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <h2 className="text-xl font-semibold capitalize">{monthName}</h2>

          <button
            onClick={nextMonth}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        {/* Calendar Grid */}
        <div className="grid grid-cols-7 gap-2">
          {/* Day headers */}
          {['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'].map(day => (
            <div key={day} className="text-center font-semibold text-gray-700 py-2">
              {day}
            </div>
          ))}

          {/* Calendar days */}
          {days.map((day, index) => {
            const dayPosts = getPostsForDate(day);
            const isToday = day?.toDateString() === new Date().toDateString();

            return (
              <div
                key={index}
                className={`min-h-[120px] border rounded-lg p-2 ${
                  day ? 'bg-white hover:bg-gray-50' : 'bg-gray-50'
                } ${isToday ? 'border-blue-500 border-2' : 'border-gray-200'}`}
              >
                {day && (
                  <>
                    <div className={`text-sm font-semibold mb-2 ${isToday ? 'text-blue-600' : 'text-gray-700'}`}>
                      {day.getDate()}
                    </div>

                    {/* Posts for this day */}
                    <div className="space-y-1">
                      {dayPosts.map(post => (
                        <div
                          key={post.id}
                          className={`text-xs p-1.5 rounded border cursor-pointer ${getStatusColor(post.status)}`}
                          onClick={() => setSelectedPost(post)}
                        >
                          <div className="font-medium truncate">{post.caption.slice(0, 30)}...</div>
                          {post.scheduled_time && (
                            <div className="text-xs opacity-75 flex items-center gap-1">
                              <Clock className="w-3 h-3" />
                              {formatTime(post.scheduled_time)}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Drafts Section */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Edit className="w-5 h-5" />
          Bài Nháp ({drafts.length})
        </h2>

        {drafts.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Chưa có bài nháp nào</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {drafts.map(draft => (
              <div
                key={draft.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="mb-3">
                  <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${getStatusColor(draft.status)}`}>
                    {getStatusLabel(draft.status)}
                  </span>
                </div>

                <p className="text-sm text-gray-700 mb-3 line-clamp-3">{draft.caption}</p>

                <div className="text-xs text-gray-500 mb-3">
                  Tạo lúc: {new Date(draft.created_at).toLocaleString('vi-VN')}
                </div>

                <div className="flex gap-2 mb-2">
                  <button
                    onClick={() => {
                      setSelectedPost(draft);
                      setShowScheduleModal(true);
                      // Set default time to tomorrow at 10:00
                      const tomorrow = new Date();
                      tomorrow.setDate(tomorrow.getDate() + 1);
                      tomorrow.setHours(10, 0, 0, 0);
                      setScheduleDateTime(tomorrow.toISOString().slice(0, 16));
                    }}
                    className="flex-1 bg-blue-500 text-white px-3 py-2 rounded-lg hover:bg-blue-600 transition-colors text-sm flex items-center justify-center gap-1"
                  >
                    <Calendar className="w-4 h-4" />
                    Lên lịch
                  </button>

                  <button
                    onClick={() => setSelectedPost(draft)}
                    className="bg-gray-100 text-gray-700 px-3 py-2 rounded-lg hover:bg-gray-200 transition-colors"
                    title="Xem chi tiết"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setSelectedPost(draft);
                      setEditCaption(draft.caption);
                      setShowEditModal(true);
                    }}
                    className="flex-1 bg-green-500 text-white px-3 py-2 rounded-lg hover:bg-green-600 transition-colors text-sm flex items-center justify-center gap-1"
                  >
                    <Edit className="w-4 h-4" />
                    Sửa
                  </button>

                  <button
                    onClick={() => handleDeletePost(draft.id)}
                    className="flex-1 bg-red-500 text-white px-3 py-2 rounded-lg hover:bg-red-600 transition-colors text-sm flex items-center justify-center gap-1"
                  >
                    <Trash2 className="w-4 h-4" />
                    Xóa
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Schedule Modal */}
      {showScheduleModal && selectedPost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-xl font-semibold mb-4">Lên Lịch Đăng Bài</h3>

            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">Caption:</p>
              <p className="text-sm bg-gray-50 p-3 rounded border border-gray-200 line-clamp-3">
                {selectedPost.caption}
              </p>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Thời gian đăng
              </label>
              <input
                type="datetime-local"
                value={scheduleDateTime}
                onChange={(e) => setScheduleDateTime(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowScheduleModal(false);
                  setSelectedPost(null);
                  setScheduleDateTime('');
                }}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Hủy
              </button>
              <button
                onClick={() => handleSchedulePost(selectedPost.id, scheduleDateTime)}
                disabled={!scheduleDateTime}
                className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                Xác nhận
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Post Detail Modal */}
      {selectedPost && !showScheduleModal && (
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
              <div>
                <span className={`inline-block px-3 py-1 rounded text-sm font-medium ${getStatusColor(selectedPost.status)}`}>
                  {getStatusLabel(selectedPost.status)}
                </span>
              </div>

              {selectedPost.image_path && (
                <div>
                  <img
                    src={`${API_URL}/uploads/${selectedPost.image_path}`}
                    alt="Post content"
                    className="w-full rounded-lg border border-gray-200"
                    onError={(e) => {
                      console.error('Failed to load image:', selectedPost.image_path);
                      e.currentTarget.style.display = 'none';
                    }}
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

              <div className="flex gap-3 pt-4 border-t">
                {selectedPost.status === 'scheduled' && (
                  <button
                    onClick={() => {
                      handleUnschedule(selectedPost.id);
                      setSelectedPost(null);
                    }}
                    className="flex-1 bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600 transition-colors"
                  >
                    Hủy Lịch (Chuyển về Nháp)
                  </button>
                )}

                {selectedPost.status === 'draft' && (
                  <>
                    <button
                      onClick={() => {
                        setEditCaption(selectedPost.caption);
                        setShowEditModal(true);
                      }}
                      className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors flex items-center gap-2"
                    >
                      <Edit className="w-4 h-4" />
                      Sửa
                    </button>
                    <button
                      onClick={() => {
                        setShowScheduleModal(true);
                        const tomorrow = new Date();
                        tomorrow.setDate(tomorrow.getDate() + 1);
                        tomorrow.setHours(10, 0, 0, 0);
                        setScheduleDateTime(tomorrow.toISOString().slice(0, 16));
                      }}
                      className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center gap-2"
                    >
                      <Calendar className="w-4 h-4" />
                      Lên Lịch
                    </button>
                    <button
                      onClick={() => handleDeletePost(selectedPost.id)}
                      className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors flex items-center gap-2"
                    >
                      <Trash2 className="w-4 h-4" />
                      Xóa
                    </button>
                  </>
                )}

                {/* Chỉ cho phép xóa bài đã posted hoặc failed */}
                {(selectedPost.status === 'posted' || selectedPost.status === 'failed') && (
                  <button
                    onClick={() => {
                      handleDeletePost(selectedPost.id);
                      setSelectedPost(null);
                    }}
                    className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors flex items-center gap-2"
                  >
                    <Trash2 className="w-4 h-4" />
                    Xóa
                  </button>
                )}

                <button
                  onClick={() => setSelectedPost(null)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Đóng
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Edit Modal */}
      {showEditModal && selectedPost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">Sửa Bài Đăng</h3>
              <button
                onClick={() => {
                  setShowEditModal(false);
                  setSelectedPost(null);
                  setEditCaption('');
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              {selectedPost.image_path && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Ảnh meme:</label>
                  <img
                    src={`${API_URL}/uploads/${selectedPost.image_path}`}
                    alt="Post content"
                    className="w-full max-h-64 object-contain rounded-lg border border-gray-200"
                    onError={(e) => {
                      console.error('Failed to load image:', selectedPost.image_path);
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Caption: <span className="text-red-500">*</span>
                </label>
                <textarea
                  value={editCaption}
                  onChange={(e) => setEditCaption(e.target.value)}
                  placeholder="Nhập caption cho bài đăng..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  rows={6}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {editCaption.length} ký tự
                </p>
              </div>

              <div className="flex gap-3 pt-4 border-t">
                <button
                  onClick={() => {
                    setShowEditModal(false);
                    setSelectedPost(null);
                    setEditCaption('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Hủy
                </button>
                <button
                  onClick={handleEditPost}
                  disabled={!editCaption.trim()}
                  className="flex-1 bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <Edit className="w-4 h-4" />
                  Lưu thay đổi
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Legend */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Chú thích:</h3>
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-gray-100 border border-gray-300 rounded"></div>
            <span className="text-sm text-gray-600">Nháp</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-100 border border-blue-300 rounded"></div>
            <span className="text-sm text-gray-600">Đã lên lịch</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-100 border border-green-300 rounded"></div>
            <span className="text-sm text-gray-600">Đã đăng</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-red-100 border border-red-300 rounded"></div>
            <span className="text-sm text-gray-600">Thất bại</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-blue-500 rounded"></div>
            <span className="text-sm text-gray-600">Hôm nay</span>
          </div>
        </div>
      </div>
    </div>
  );
}
