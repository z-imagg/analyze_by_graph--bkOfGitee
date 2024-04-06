// 【术语】 最后fnCallId==最大fnCallId==终点fnCallId,  最开始fnCallId==最小fnCallId==起点fnCallId
// 已上一个 孤立群 的 终点fnCallId, 求 下一个孤立群 的 起点fnCallId
with $previous_end_fnCallId as  previous_end_fnCallId
match (v:V_FnCallLog {direct:1})
where v.fnCallId > previous_end_fnCallId
return min(v.fnCallId) as next_begin_fnCallId