-- Pandoc Lua filter: keep table titles together with their tables
-- Wraps "Table N." or "Table N:" paragraph + table + "Note(s)" paragraph in unbreakable block
-- Supports both bold ("**Table N.**") and plain ("Table N:") caption formats

local function is_table_caption(block)
  if block.t ~= "Para" or #block.content == 0 then
    return false
  end
  local first = block.content[1]
  -- Match bold format: **Table N.**
  if first.t == "Strong" then
    local strong_text = pandoc.utils.stringify(first)
    if strong_text:match("^Table%s+%d") then
      return true
    end
  end
  -- Match plain format: Table N: or Table N.
  local full_text = pandoc.utils.stringify(block)
  if full_text:match("^Table%s+%d") then
    return true
  end
  return false
end

local function is_table_note(block)
  if block.t ~= "Para" then
    return false
  end
  local text = pandoc.utils.stringify(block)
  return text:match("^Note%.") or text:match("^Note:") or text:match("^Notes") or text:match("^Key:")
end

function Blocks(blocks)
  local result = {}
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    if is_table_caption(block) then
      -- Collect: title para, table, optional note para
      local group = {}
      table.insert(group, pandoc.RawBlock("typst", "#block(breakable: false)["))
      table.insert(group, block)  -- title
      -- Look for table and note after
      local j = i + 1
      while j <= #blocks do
        local next_block = blocks[j]
        if next_block.t == "Table" then
          table.insert(group, next_block)
          j = j + 1
        elseif is_table_note(next_block) then
          table.insert(group, next_block)
          j = j + 1
          break  -- note is the last element in group
        else
          break
        end
      end
      table.insert(group, pandoc.RawBlock("typst", "]"))
      for _, g in ipairs(group) do
        table.insert(result, g)
      end
      i = j
    else
      table.insert(result, block)
      i = i + 1
    end
  end
  return result
end
