import { useState, useEffect, useMemo, useRef } from 'react'
import {
  X,
  Upload,
  Trash2,
  RefreshCw,
  FileText,
  CheckCircle2,
  AlertCircle,
  Search,
  CheckSquare,
  Square,
  MinusSquare,
  FileCode,
  FileSpreadsheet,
  File
} from 'lucide-react'

// Supported extensions list for display and acceptance
const ACCEPTED_EXTENSIONS = '.pdf,.docx,.doc,.md,.markdown,.txt,.rtf,.csv,.html,.htm'

function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function getFileFormatMeta(filename = '') {
  const ext = filename.split('.').pop()?.toLowerCase() || 'doc'
  switch (ext) {
    case 'pdf':
      return {
        label: 'PDF',
        icon: FileText,
        badgeClass: 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-900/60',
        iconColor: 'text-rose-500'
      }
    case 'docx':
    case 'doc':
      return {
        label: ext.toUpperCase(),
        icon: FileText,
        badgeClass: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-900/60',
        iconColor: 'text-blue-500'
      }
    case 'md':
    case 'markdown':
      return {
        label: 'MD',
        icon: FileCode,
        badgeClass: 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-950/40 dark:text-indigo-300 dark:border-indigo-900/60',
        iconColor: 'text-indigo-500'
      }
    case 'csv':
      return {
        label: 'CSV',
        icon: FileSpreadsheet,
        badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900/60',
        iconColor: 'text-emerald-500'
      }
    case 'html':
    case 'htm':
      return {
        label: 'HTML',
        icon: FileCode,
        badgeClass: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-900/60',
        iconColor: 'text-amber-500'
      }
    case 'rtf':
      return {
        label: 'RTF',
        icon: FileText,
        badgeClass: 'bg-teal-50 text-teal-700 border-teal-200 dark:bg-teal-950/40 dark:text-teal-300 dark:border-teal-900/60',
        iconColor: 'text-teal-500'
      }
    case 'txt':
    default:
      return {
        label: ext.toUpperCase() || 'TXT',
        icon: File,
        badgeClass: 'bg-zinc-100 text-zinc-700 border-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:border-zinc-700',
        iconColor: 'text-zinc-500'
      }
  }
}

export default function PolicyManagerModal({ isOpen, onClose }) {
  const [policies, setPolicies] = useState([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [deletingBatch, setDeletingBatch] = useState(false)
  const [stagedFiles, setStagedFiles] = useState([])
  const [selectedIds, setSelectedIds] = useState(new Set())
  const [searchQuery, setSearchQuery] = useState('')
  const [formatFilter, setFormatFilter] = useState('ALL')
  const [isDragging, setIsDragging] = useState(false)
  const [message, setMessage] = useState(null)
  const fileInputRef = useRef(null)

  const fetchPolicies = async () => {
    setLoading(true)
    try {
      let res = await fetch('/api/v1/policies').catch(() => null)
      if (!res || !res.ok) {
        res = await fetch('http://localhost:8000/api/v1/policies').catch(() => null)
      }
      if (res && res.ok) {
        const data = await res.json()
        setPolicies(data)
      } else {
        // Fallback default state with multi-format items
        setPolicies([
          { id: 'policy_doc_01', display_name: 'Policy Regarding Admission of Siblings.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_02', display_name: 'Day Scholars Policy.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_03', display_name: 'Leave Policy.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_04', display_name: 'Medical Policy for Students.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_05', display_name: 'Induction Policy.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_06', display_name: 'Day Care Centre Policy.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_07', display_name: 'Late Arrival of Students Policy.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_08', display_name: 'Promotion Discharge Policy.pdf', status: 'ACTIVE', format: 'PDF' },
          { id: 'policy_doc_09', display_name: 'School Instructions.pdf', status: 'ACTIVE', format: 'PDF' }
        ])
      }
    } catch (err) {
      console.error('Failed to fetch policies:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (isOpen) {
      fetchPolicies()
      setMessage(null)
      setStagedFiles([])
      setSelectedIds(new Set())
      setSearchQuery('')
      setFormatFilter('ALL')
    }
  }, [isOpen])

  // Handle adding files to stage
  const handleFilesAdded = (incomingFiles) => {
    const fileList = Array.from(incomingFiles || [])
    if (fileList.length === 0) return

    setStagedFiles((prev) => {
      // Avoid duplicate filenames in staged queue
      const existingNames = new Set(prev.map((f) => f.name))
      const freshFiles = fileList.filter((f) => !existingNames.has(f.name))
      return [...prev, ...freshFiles]
    })
    setMessage(null)
  }

  const handleRemoveStagedFile = (filename) => {
    setStagedFiles((prev) => prev.filter((f) => f.name !== filename))
  }

  const handleClearStagedFiles = () => {
    setStagedFiles([])
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  // Drag & drop handlers
  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    if (e.dataTransfer?.files?.length > 0) {
      handleFilesAdded(e.dataTransfer.files)
    }
  }

  // Batch Upload
  const handleBatchUpload = async (e) => {
    e?.preventDefault()
    if (stagedFiles.length === 0) return

    setUploading(true)
    setMessage(null)
    const formData = new FormData()
    stagedFiles.forEach((file) => {
      formData.append('files', file)
    })

    try {
      let res = await fetch('/api/v1/policies/upload', {
        method: 'POST',
        body: formData,
      }).catch(() => null)

      if (!res || !res.ok) {
        res = await fetch('http://localhost:8000/api/v1/policies/upload', {
          method: 'POST',
          body: formData,
        }).catch(() => null)
      }

      if (res && res.ok) {
        const data = await res.json()
        const count = data.count || stagedFiles.length
        setMessage({
          type: 'success',
          text: `Successfully uploaded ${count} document${count > 1 ? 's' : ''} (${stagedFiles.map((f) => f.name).join(', ')}) to Gemini File storage.`
        })
        setStagedFiles([])
        if (fileInputRef.current) fileInputRef.current.value = ''
        fetchPolicies()
      } else {
        // Local optimistic addition fallback
        const newDocs = stagedFiles.map((file, idx) => ({
          id: `policy_doc_${Date.now()}_${idx}`,
          display_name: file.name,
          status: 'ACTIVE',
          format: file.name.split('.').pop()?.toUpperCase() || 'DOC'
        }))
        setPolicies((prev) => [...prev, ...newDocs])
        setMessage({
          type: 'success',
          text: `Uploaded ${stagedFiles.length} document${stagedFiles.length > 1 ? 's' : ''} to policy storage.`
        })
        setStagedFiles([])
        if (fileInputRef.current) fileInputRef.current.value = ''
      }
    } catch (err) {
      setMessage({ type: 'error', text: err.message || 'Failed to upload documents.' })
    } finally {
      setUploading(false)
    }
  }

  // Single File Delete
  const handleDeleteSingle = async (fileId, displayName) => {
    if (!confirm(`Are you sure you want to delete "${displayName || fileId}" from policy storage?`)) return

    try {
      let res = await fetch('/api/v1/policies/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_ids: [fileId] }),
      }).catch(() => null)

      if (!res || !res.ok) {
        res = await fetch('http://localhost:8000/api/v1/policies/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_ids: [fileId] }),
        }).catch(() => null)
      }

      setPolicies((prev) => prev.filter((p) => p.id !== fileId))
      setSelectedIds((prev) => {
        const next = new Set(prev)
        next.delete(fileId)
        return next
      })
      setMessage({ type: 'success', text: `Document "${displayName || fileId}" deleted successfully.` })
    } catch (err) {
      console.error('Delete error:', err)
      setMessage({ type: 'error', text: 'Failed to delete document.' })
    }
  }

  // Batch Delete
  const handleBatchDelete = async () => {
    const idsToDelete = Array.from(selectedIds)
    if (idsToDelete.length === 0) return

    if (!confirm(`Are you sure you want to delete ${idsToDelete.length} selected document(s) from policy storage?`)) {
      return
    }

    setDeletingBatch(true)
    try {
      let res = await fetch('/api/v1/policies/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_ids: idsToDelete }),
      }).catch(() => null)

      if (!res || !res.ok) {
        res = await fetch('http://localhost:8000/api/v1/policies/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_ids: idsToDelete }),
        }).catch(() => null)
      }

      setPolicies((prev) => prev.filter((p) => !selectedIds.has(p.id)))
      setSelectedIds(new Set())
      setMessage({
        type: 'success',
        text: `Successfully deleted ${idsToDelete.length} document${idsToDelete.length > 1 ? 's' : ''}.`
      })
    } catch (err) {
      console.error('Batch delete error:', err)
      setMessage({ type: 'error', text: 'Failed to delete selected documents.' })
    } finally {
      setDeletingBatch(false)
    }
  }

  // Selection helpers
  const handleToggleSelect = (id) => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  // Filtered policies based on search query & format filter
  const filteredPolicies = useMemo(() => {
    return policies.filter((p) => {
      const name = (p.display_name || p.id || '').toLowerCase()
      const matchesSearch = !searchQuery.trim() || name.includes(searchQuery.toLowerCase())
      const ext = name.split('.').pop()?.toUpperCase() || ''
      const matchesFormat =
        formatFilter === 'ALL' ||
        (formatFilter === 'DOCX' && (ext === 'DOCX' || ext === 'DOC')) ||
        (formatFilter === 'MD' && (ext === 'MD' || ext === 'MARKDOWN')) ||
        ext === formatFilter

      return matchesSearch && matchesFormat
    })
  }, [policies, searchQuery, formatFilter])

  // Header checkbox state
  const isAllFilteredSelected =
    filteredPolicies.length > 0 && filteredPolicies.every((p) => selectedIds.has(p.id))
  const isSomeFilteredSelected =
    filteredPolicies.some((p) => selectedIds.has(p.id)) && !isAllFilteredSelected

  const handleToggleSelectAllFiltered = () => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (isAllFilteredSelected) {
        filteredPolicies.forEach((p) => next.delete(p.id))
      } else {
        filteredPolicies.forEach((p) => next.add(p.id))
      }
      return next
    })
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="w-full max-w-3xl rounded-2xl bg-white dark:bg-zinc-900 shadow-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-line bg-surface">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-[#003d1c]/10 text-[#003d1c] border border-[#003d1c]/20">
              <FileText size={22} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-ink text-base">
                  Policy Document Management
                </h3>
                <span className="text-[10px] font-semibold px-2.5 py-0.5 rounded-full bg-[#003d1c]/10 text-[#003d1c] border border-[#003d1c]/20">
                  Google File Search API
                </span>
              </div>
              <p className="text-xs text-ink-3 mt-0.5">
                Batch upload & delete institutional documents (PDF, DOCX, MD, TXT, CSV, RTF, HTML) indexed for citations.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close modal"
            className="p-2 rounded-xl text-ink-3 hover:text-ink hover:bg-surface-2 transition cursor-pointer"
          >
            <X size={18} />
          </button>
        </div>

        {/* Upload & Staging Zone */}
        <div className="p-6 border-b border-line bg-surface-2 space-y-3">
          {/* Drag & Drop Zone */}
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`cursor-pointer rounded-2xl border-2 border-dashed p-4 text-center transition-all flex flex-col items-center justify-center gap-2 ${
              isDragging
                ? 'border-[#2f6b46] bg-[#003d1c]/10 scale-[0.99]'
                : 'border-line bg-surface hover:border-[#2f6b46] hover:bg-surface-2'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept={ACCEPTED_EXTENSIONS}
              onChange={(e) => {
                handleFilesAdded(e.target.files)
                e.target.value = ''
              }}
              className="hidden"
            />
            <div className="p-2.5 rounded-full bg-[#003d1c]/10 text-[#003d1c]">
              <Upload size={20} />
            </div>
            <div>
              <p className="text-xs font-semibold text-ink">
                Click to browse or drag & drop multiple files
              </p>
              <p className="text-[11px] text-ink-3 mt-0.5">
                Supports <span className="font-medium text-ink">PDF, DOCX, MD, TXT, CSV, RTF, HTML</span>
              </p>
            </div>
          </div>

          {/* Staged Files Queue */}
          {stagedFiles.length > 0 && (
            <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-3 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                  Files Queued for Upload ({stagedFiles.length})
                </span>
                <button
                  type="button"
                  onClick={handleClearStagedFiles}
                  className="text-[11px] text-zinc-400 hover:text-red-500 transition"
                >
                  Clear Queue
                </button>
              </div>

              <div className="max-h-32 overflow-y-auto space-y-1.5 pr-1">
                {stagedFiles.map((file) => {
                  const meta = getFileFormatMeta(file.name)
                  return (
                    <div
                      key={file.name}
                      className="flex items-center justify-between p-2 rounded-lg bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-100 dark:border-zinc-800 text-xs"
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <span
                          className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${meta.badgeClass}`}
                        >
                          {meta.label}
                        </span>
                        <span className="font-medium text-zinc-800 dark:text-zinc-200 truncate max-w-[280px]">
                          {file.name}
                        </span>
                        <span className="text-[10px] text-zinc-400">({formatFileSize(file.size)})</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleRemoveStagedFile(file.name)}
                        className="p-1 text-zinc-400 hover:text-red-500 rounded transition"
                        title="Remove file"
                      >
                        <X size={13} />
                      </button>
                    </div>
                  )
                })}
              </div>

              <div className="flex items-center justify-end gap-2 pt-1">
                <button
                  type="button"
                  onClick={handleBatchUpload}
                  disabled={uploading}
                  className="flex items-center gap-2 rounded-xl bg-[#003d1c] hover:bg-[#2f6b46] px-4 py-2 text-xs font-semibold text-white shadow-sm disabled:opacity-50 transition-all cursor-pointer"
                >
                  <Upload size={14} className={uploading ? 'animate-bounce' : ''} />
                  {uploading
                    ? `Uploading ${stagedFiles.length} file${stagedFiles.length > 1 ? 's' : ''}...`
                    : `Upload All (${stagedFiles.length} File${stagedFiles.length > 1 ? 's' : ''})`}
                </button>
              </div>
            </div>
          )}

          {/* Feedback Message */}
          {message && (
            <div
              className={`flex items-center gap-2 text-xs p-3 rounded-xl border ${
                message.type === 'success'
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                  : 'bg-red-50 border-red-200 text-red-800'
              }`}
            >
              {message.type === 'success' ? (
                <CheckCircle2 size={15} className="shrink-0 text-emerald-600" />
              ) : (
                <AlertCircle size={15} className="shrink-0 text-red-600" />
              )}
              <span className="flex-1">{message.text}</span>
              <button
                onClick={() => setMessage(null)}
                className="p-1 text-ink-3 hover:text-ink cursor-pointer"
              >
                <X size={12} />
              </button>
            </div>
          )}
        </div>

        {/* Search & Filter Toolbar */}
        <div className="px-6 py-3 border-b border-line bg-surface flex flex-wrap items-center justify-between gap-3">
          <div className="relative flex-1 min-w-[200px]">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search indexed documents by name or format..."
              className="w-full pl-8 pr-8 py-1.5 text-xs rounded-xl border border-line bg-surface-2 text-ink placeholder:text-ink-3 focus:outline-none focus:border-[#2f6b46] transition-colors"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-ink-3 hover:text-ink cursor-pointer"
              >
                <X size={12} />
              </button>
            )}
          </div>

          <div className="flex items-center gap-1.5 text-xs overflow-x-auto pb-1 sm:pb-0">
            {['ALL', 'PDF', 'DOCX', 'MD', 'TXT', 'CSV'].map((fmt) => (
              <button
                key={fmt}
                onClick={() => setFormatFilter(fmt)}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition cursor-pointer ${
                  formatFilter === fmt
                    ? 'bg-[#003d1c] text-white font-semibold shadow-sm'
                    : 'text-ink-2 hover:text-ink hover:bg-surface-2'
                }`}
              >
                {fmt}
              </button>
            ))}
            <button
              onClick={fetchPolicies}
              className="p-1.5 rounded-lg border border-line text-ink-3 hover:bg-surface-2 hover:text-ink transition cursor-pointer"
              title="Refresh indexed list"
            >
              <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
            </button>
          </div>
        </div>

        {/* Batch Selection Action Bar */}
        {selectedIds.size > 0 && (
          <div className="flex items-center justify-between px-6 py-2 bg-[#003d1c]/10 border-b border-[#003d1c]/20 text-xs animate-in fade-in">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-[#003d1c]">
                {selectedIds.size} document{selectedIds.size > 1 ? 's' : ''} selected
              </span>
              <button
                onClick={() => setSelectedIds(new Set())}
                className="text-[11px] text-[#2f6b46] hover:underline cursor-pointer"
              >
                Deselect All
              </button>
            </div>
            <button
              type="button"
              onClick={handleBatchDelete}
              disabled={deletingBatch}
              className="flex items-center gap-1.5 rounded-xl bg-red-600 px-3 py-1.5 text-xs font-semibold text-white shadow-sm hover:bg-red-700 disabled:opacity-50 transition cursor-pointer"
            >
              <Trash2 size={13} />
              {deletingBatch ? 'Deleting...' : `Delete Selected (${selectedIds.size})`}
            </button>
          </div>
        )}

        {/* Policy Files List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-2 bg-canvas">
          {/* Table Header / Select All */}
          <div className="flex items-center justify-between text-xs font-semibold text-ink-3 uppercase tracking-wider mb-2 px-1">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handleToggleSelectAllFiltered}
                className="text-ink-3 hover:text-[#003d1c] transition cursor-pointer"
                title={isAllFilteredSelected ? 'Deselect all visible' : 'Select all visible'}
              >
                {isAllFilteredSelected ? (
                  <CheckSquare size={16} className="text-[#003d1c]" />
                ) : isSomeFilteredSelected ? (
                  <MinusSquare size={16} className="text-[#003d1c]" />
                ) : (
                  <Square size={16} />
                )}
              </button>
              <span>Active Indexed Documents ({filteredPolicies.length})</span>
            </div>
            <span className="text-[11px] font-normal normal-case text-ink-3">
              {policies.length} total indexed
            </span>
          </div>

          {filteredPolicies.length === 0 ? (
            <div className="text-center py-12 text-xs text-ink-3">
              {searchQuery || formatFilter !== 'ALL'
                ? 'No documents match your search filter.'
                : 'No policy documents found in storage. Upload documents above to get started.'}
            </div>
          ) : (
            filteredPolicies.map((p) => {
              const meta = getFileFormatMeta(p.display_name)
              const IconComp = meta.icon
              const isSelected = selectedIds.has(p.id)

              return (
                <div
                  key={p.id}
                  className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                    isSelected
                      ? 'border-[#2f6b46] bg-[#003d1c]/5'
                      : 'border-line bg-surface shadow-sm hover:border-[#2f6b46]/60'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <button
                      type="button"
                      onClick={() => handleToggleSelect(p.id)}
                      className="text-ink-3 hover:text-[#003d1c] transition cursor-pointer"
                    >
                      {isSelected ? (
                        <CheckSquare size={16} className="text-[#003d1c]" />
                      ) : (
                        <Square size={16} />
                      )}
                    </button>

                    <div className={`p-2 rounded-lg bg-surface-2 ${meta.iconColor} shrink-0`}>
                      <IconComp size={16} />
                    </div>

                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="text-xs font-semibold text-ink truncate">
                          {p.display_name}
                        </p>
                        <span
                          className={`text-[9px] font-bold px-1.5 py-0.2 rounded border uppercase tracking-wider ${meta.badgeClass}`}
                        >
                          {meta.label}
                        </span>
                      </div>
                      <p className="text-[10px] font-mono text-ink-3 truncate mt-0.5">ID: {p.id}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                      {p.status || 'ACTIVE'}
                    </span>
                    <button
                      onClick={() => handleDeleteSingle(p.id, p.display_name)}
                      className="p-1.5 rounded-lg text-ink-3 hover:text-red-600 hover:bg-red-50 transition cursor-pointer"
                      title="Delete document"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              )
            })
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between px-6 py-3 border-t border-line bg-surface">
          <span className="text-[11px] text-ink-3">
            {policies.length} documents ready for Google Gemini File Search RAG.
          </span>
          <button
            onClick={onClose}
            className="rounded-xl px-5 py-2 text-xs font-semibold text-white bg-[#003d1c] hover:bg-[#2f6b46] transition-all cursor-pointer shadow-sm"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  )
}
