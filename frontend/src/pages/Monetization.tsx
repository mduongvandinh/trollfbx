import { useState, useEffect } from 'react';
import axios from 'axios';
import { DollarSign, TrendingUp, Link as LinkIcon, Plus, Edit, Trash2, BarChart3, ExternalLink } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface AffiliateCampaign {
  id: number;
  name: string;
  product_type: string;
  affiliate_link: string;
  commission_rate: number;
  clicks: number;
  conversions: number;
  revenue: number;
  is_active: boolean;
  created_at: string;
}

export default function Monetization() {
  const [campaigns, setCampaigns] = useState<AffiliateCampaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingCampaign, setEditingCampaign] = useState<AffiliateCampaign | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    product_type: 'jersey',
    affiliate_link: '',
    commission_rate: 0
  });

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/monetization/campaigns`);
      setCampaigns(response.data);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (editingCampaign) {
        await axios.put(`${API_URL}/api/monetization/campaigns/${editingCampaign.id}`, formData);
      } else {
        await axios.post(`${API_URL}/api/monetization/campaigns`, formData);
      }

      setShowAddModal(false);
      setEditingCampaign(null);
      setFormData({ name: '', product_type: 'jersey', affiliate_link: '', commission_rate: 0 });
      await fetchCampaigns();
    } catch (error) {
      console.error('Error saving campaign:', error);
      alert('Lỗi khi lưu chiến dịch');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Bạn có chắc muốn xóa chiến dịch này?')) return;

    try {
      await axios.delete(`${API_URL}/api/monetization/campaigns/${id}`);
      await fetchCampaigns();
    } catch (error) {
      console.error('Error deleting campaign:', error);
      alert('Lỗi khi xóa chiến dịch');
    }
  };

  const handleToggleActive = async (id: number, isActive: boolean) => {
    try {
      await axios.put(`${API_URL}/api/monetization/campaigns/${id}`, { is_active: !isActive });
      await fetchCampaigns();
    } catch (error) {
      console.error('Error toggling campaign:', error);
    }
  };

  const openEditModal = (campaign: AffiliateCampaign) => {
    setEditingCampaign(campaign);
    setFormData({
      name: campaign.name,
      product_type: campaign.product_type,
      affiliate_link: campaign.affiliate_link,
      commission_rate: campaign.commission_rate
    });
    setShowAddModal(true);
  };

  const totalRevenue = campaigns.reduce((sum, c) => sum + c.revenue, 0);
  const totalClicks = campaigns.reduce((sum, c) => sum + c.clicks, 0);
  const totalConversions = campaigns.reduce((sum, c) => sum + c.conversions, 0);
  const avgConversionRate = totalClicks > 0 ? (totalConversions / totalClicks) * 100 : 0;

  const productTypeLabels: Record<string, string> = {
    jersey: 'Áo đấu',
    app: 'Ứng dụng',
    betting: 'Cá cược',
    merchandise: 'Hàng lưu niệm',
    streaming: 'Xem bóng đá',
    other: 'Khác'
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <DollarSign className="w-8 h-8 text-green-600" />
            Kiếm Tiền
          </h1>
          <p className="text-gray-600 mt-2">Quản lý chiến dịch affiliate marketing</p>
        </div>

        <button
          onClick={() => {
            setEditingCampaign(null);
            setFormData({ name: '', product_type: 'jersey', affiliate_link: '', commission_rate: 0 });
            setShowAddModal(true);
          }}
          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Thêm Chiến Dịch
        </button>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tổng Doanh Thu</div>
            <DollarSign className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{totalRevenue.toLocaleString()}đ</div>
          <div className="text-sm text-gray-500 mt-1">Từ {campaigns.length} chiến dịch</div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tổng Clicks</div>
            <LinkIcon className="w-5 h-5 text-blue-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{totalClicks.toLocaleString()}</div>
          <div className="text-sm text-gray-500 mt-1">Lượt nhấp vào link</div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Chuyển Đổi</div>
            <TrendingUp className="w-5 h-5 text-purple-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{totalConversions}</div>
          <div className="text-sm text-gray-500 mt-1">Đơn hàng thành công</div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tỷ Lệ Chuyển Đổi</div>
            <BarChart3 className="w-5 h-5 text-orange-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{avgConversionRate.toFixed(1)}%</div>
          <div className="text-sm text-gray-500 mt-1">Trung bình</div>
        </div>
      </div>

      {/* Campaigns List */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4">Danh Sách Chiến Dịch</h2>

        {campaigns.length === 0 ? (
          <div className="text-center py-12">
            <DollarSign className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 mb-4">Chưa có chiến dịch nào</p>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              Tạo Chiến Dịch Đầu Tiên
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {campaigns.map(campaign => (
              <div
                key={campaign.id}
                className={`border rounded-lg p-4 transition-all ${
                  campaign.is_active
                    ? 'border-gray-200 bg-white'
                    : 'border-gray-200 bg-gray-50 opacity-60'
                }`}
              >
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{campaign.name}</h3>
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">
                        {productTypeLabels[campaign.product_type] || campaign.product_type}
                      </span>
                      <span
                        className={`px-2 py-1 text-xs rounded ${
                          campaign.is_active
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        {campaign.is_active ? 'Đang chạy' : 'Tạm dừng'}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                      <LinkIcon className="w-4 h-4" />
                      <a
                        href={campaign.affiliate_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:text-blue-600 hover:underline flex items-center gap-1"
                      >
                        {campaign.affiliate_link.slice(0, 50)}...
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>

                    <div className="text-sm text-gray-600">
                      Hoa hồng: <span className="font-semibold">{campaign.commission_rate}%</span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => handleToggleActive(campaign.id, campaign.is_active)}
                      className={`px-3 py-2 rounded-lg transition-colors text-sm ${
                        campaign.is_active
                          ? 'bg-yellow-50 text-yellow-700 hover:bg-yellow-100'
                          : 'bg-green-50 text-green-700 hover:bg-green-100'
                      }`}
                    >
                      {campaign.is_active ? 'Tạm dừng' : 'Kích hoạt'}
                    </button>

                    <button
                      onClick={() => openEditModal(campaign)}
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      <Edit className="w-4 h-4" />
                    </button>

                    <button
                      onClick={() => handleDelete(campaign.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-4 gap-4 pt-3 border-t border-gray-200">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Clicks</div>
                    <div className="text-lg font-semibold text-gray-900">{campaign.clicks}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Chuyển đổi</div>
                    <div className="text-lg font-semibold text-gray-900">{campaign.conversions}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Tỷ lệ</div>
                    <div className="text-lg font-semibold text-gray-900">
                      {campaign.clicks > 0 ? ((campaign.conversions / campaign.clicks) * 100).toFixed(1) : '0'}%
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Doanh thu</div>
                    <div className="text-lg font-semibold text-green-600">{campaign.revenue.toLocaleString()}đ</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add/Edit Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-xl font-semibold mb-4">
              {editingCampaign ? 'Chỉnh Sửa Chiến Dịch' : 'Thêm Chiến Dịch Mới'}
            </h3>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Tên chiến dịch</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="VD: Áo đấu MU 2024"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Loại sản phẩm</label>
                <select
                  value={formData.product_type}
                  onChange={(e) => setFormData({ ...formData, product_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="jersey">Áo đấu</option>
                  <option value="app">Ứng dụng</option>
                  <option value="betting">Cá cược</option>
                  <option value="merchandise">Hàng lưu niệm</option>
                  <option value="streaming">Xem bóng đá</option>
                  <option value="other">Khác</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Link affiliate</label>
                <input
                  type="url"
                  value={formData.affiliate_link}
                  onChange={(e) => setFormData({ ...formData, affiliate_link: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="https://..."
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Tỷ lệ hoa hồng (%)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.commission_rate}
                  onChange={(e) => setFormData({ ...formData, commission_rate: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="10"
                  required
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowAddModal(false);
                    setEditingCampaign(null);
                    setFormData({ name: '', product_type: 'jersey', affiliate_link: '', commission_rate: 0 });
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                >
                  {editingCampaign ? 'Cập nhật' : 'Thêm'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Info Note */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-sm text-yellow-800">
          <strong>Lưu ý:</strong> Để link affiliate hoạt động, bạn cần tích hợp link tracking service hoặc sử dụng
          shortened URLs với UTM parameters. Dữ liệu clicks và conversions hiện đang là mô phỏng.
        </p>
      </div>
    </div>
  );
}
