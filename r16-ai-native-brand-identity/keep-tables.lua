-- Pandoc Lua filter: keep table titles together with their tables
-- Wraps "Table N." paragraph + table + "Note." paragraph in unbreakable block

function Blocks(blocks)
  local result = {}
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    -- Check if this is a Para starting with bold "Table"
    if block.t == "Para" and #block.content > 0 then
      local first = block.content[1]
      if first.t == "Strong" then
        local strong_text = pandoc.utils.stringify(first)
        if strong_text:match("^Table%s+%d") then
          -- Collect: title para, table, optional note para
          local group = {}
          -- Add raw typst block open
          table.insert(group, pandoc.RawBlock("typst", "#block(breakable: false)["))
          table.insert(group, block)  -- title
          -- Look for table and note after
          local j = i + 1
          while j <= #blocks do
            local next_block = blocks[j]
            if next_block.t == "Table" then
              table.insert(group, next_block)
              j = j + 1
            elseif next_block.t == "Para" then
              local next_text = pandoc.utils.stringify(next_block)
              if next_text:match("^Note%.") or next_text:match("^Note:") then
                table.insert(group, next_block)
                j = j + 1
                break  -- note is the last element in group
              else
                break
              end
            else
              break
            end
          end
          -- Close raw typst block
          table.insert(group, pandoc.RawBlock("typst", "]"))
          -- Add all group elements to result
          for _, g in ipairs(group) do
            table.insert(result, g)
          end
          i = j
        else
          table.insert(result, block)
          i = i + 1
        end
      else
        table.insert(result, block)
        i = i + 1
      end
    else
      table.insert(result, block)
      i = i + 1
    end
  end
  return result
end
