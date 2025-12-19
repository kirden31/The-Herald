function initMutuallyExclusiveFields(config) {
  const { primary, secondary } = config;

   function hasAnyValue($elements) {
    let hasValue = false;

    $elements.each(function () {
      const val = $(this).val();
      if (val && val.length > 0) {
        hasValue = true;
        return false; // break each
      }
    });

    return hasValue;
  }

  function updateState() {
    const hasPrimary   = hasAnyValue(primary);
    const hasSecondary = hasAnyValue(secondary);

    if (hasPrimary) {
      secondary.val(null).prop('disabled', true).trigger('change.select2');
    } else {
      secondary.prop('disabled', false).trigger('change.select2');
    }

    if (hasSecondary) {
      primary.val(null).prop('disabled', true).trigger('change.select2');
    } else {
      primary.prop('disabled', false).trigger('change.select2');
    }
  }

  primary.on('change', updateState);
  secondary.on('change', updateState);

  updateState();
}